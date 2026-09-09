import json
from datetime import UTC, datetime

from dateutil import parser as dtparser
from openai import AsyncOpenAI
from sqlalchemy import select

from app.core.config import get_settings
from app.db.models import Conversation, Message, Reservation, Restaurant
from app.integrations.reservations import get_reservation_adapter
from app.services.rag import search_knowledge

settings=get_settings()
client=AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

TOOLS=[
 {"type":"function","name":"search_restaurant_knowledge","description":"Search only this restaurant's verified knowledge for menu, allergens, hours, policies, location or other facts.","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"],"additionalProperties":False}},
 {"type":"function","name":"check_availability","description":"Check table availability before offering or booking a table.","parameters":{"type":"object","properties":{"start_at":{"type":"string","description":"ISO 8601 local datetime"},"party_size":{"type":"integer","minimum":1},"seating":{"type":["string","null"]}},"required":["start_at","party_size","seating"],"additionalProperties":False}},
 {"type":"function","name":"create_reservation","description":"Create a reservation only after the guest has supplied name, date/time and party size and has clearly requested booking.","parameters":{"type":"object","properties":{"guest_name":{"type":"string"},"guest_phone":{"type":["string","null"]},"guest_email":{"type":["string","null"]},"start_at":{"type":"string"},"party_size":{"type":"integer"},"seating":{"type":["string","null"]},"notes":{"type":["string","null"]}},"required":["guest_name","guest_phone","guest_email","start_at","party_size","seating","notes"],"additionalProperties":False}},
 {"type":"function","name":"handoff_to_staff","description":"Escalate requests requiring human confirmation, including severe allergy assurances, complaints, emergencies, groups over policy limits or uncertain facts.","parameters":{"type":"object","properties":{"reason":{"type":"string"},"summary":{"type":"string"}},"required":["reason","summary"],"additionalProperties":False}}
]

async def _tool(db, restaurant, name, args):
    if name=="search_restaurant_knowledge": return await search_knowledge(db,restaurant.id,args["query"])
    adapter=get_reservation_adapter(restaurant)
    if name=="check_availability":
        return await adapter.check(restaurant,dtparser.isoparse(args["start_at"]),args["party_size"],args.get("seating"))
    if name=="create_reservation":
        start=dtparser.isoparse(args["start_at"])
        check=await adapter.check(restaurant,start,args["party_size"],args.get("seating"))
        if not check.get("available"): return {"ok":False,"error":"not_available","availability":check}
        result=await adapter.create(restaurant,args)
        if result.get("ok",True):
            db.add(Reservation(restaurant_id=restaurant.id,provider_id=result.get("provider_id"),guest_name=args["guest_name"],guest_phone=args.get("guest_phone"),guest_email=args.get("guest_email"),party_size=args["party_size"],start_at=start,seating=args.get("seating"),notes=args.get("notes")))
            await db.commit()
        return result
    if name=="handoff_to_staff": return {"ok":True,"handoff":True,"message":"The restaurant team will follow up.",**args}
    return {"error":"unknown_tool"}

async def get_or_create_conversation(db, restaurant_id, channel, external_user_id, external_session_id=None):
    stmt=select(Conversation).where(Conversation.restaurant_id==restaurant_id,Conversation.channel==channel,Conversation.external_user_id==external_user_id)
    if external_session_id: stmt=stmt.where(Conversation.external_session_id==external_session_id)
    c=(await db.execute(stmt.order_by(Conversation.updated_at.desc()))).scalars().first()
    if not c:
        c=Conversation(restaurant_id=restaurant_id,channel=channel,external_user_id=external_user_id,external_session_id=external_session_id); db.add(c); await db.commit(); await db.refresh(c)
    return c

async def run_agent(db, restaurant: Restaurant, conversation: Conversation, user_text: str) -> str:
    db.add(Message(conversation_id=conversation.id, role="user", content=user_text)); await db.commit()
    hist=(await db.execute(select(Message).where(Message.conversation_id==conversation.id).order_by(Message.created_at.desc()).limit(12))).scalars().all()
    history="\n".join(f"{m.role}: {m.content}" for m in reversed(hist))
    if not client:
        facts=await search_knowledge(db,restaurant.id,user_text,3)
        answer="Demo mode (no OPENAI_API_KEY). Relevant restaurant facts:\n"+"\n".join("- "+x["content"] for x in facts)
    else:
        instructions=f"""You are the digital front desk for {restaurant.name}, timezone {restaurant.timezone}. Be warm, concise, multilingual and operational. At the start of a new voice interaction disclose that you are an AI/digital assistant; never pretend to be human. Never invent restaurant facts: use search_restaurant_knowledge. Never give absolute medical/allergy safety guarantees; escalate severe allergy requests. Always check availability before creating reservations. For consequential actions, reflect the exact date, time, party size and guest name in the confirmation. Use the guest's language. Current date/time context: {datetime.now(UTC).isoformat()}."""
        input_items=[{"role":"user","content":history}]
        r=await client.responses.create(model=settings.openai_model,instructions=instructions,input=input_items,tools=TOOLS,tool_choice="auto")
        for _ in range(5):
            calls=[x for x in r.output if getattr(x,"type",None)=="function_call"]
            if not calls: break
            outputs=[]
            for call in calls:
                args=json.loads(call.arguments); result=await _tool(db,restaurant,call.name,args)
                outputs.append({"type":"function_call_output","call_id":call.call_id,"output":json.dumps(result,default=str)})
            r=await client.responses.create(model=settings.openai_model,instructions=instructions,previous_response_id=r.id,input=outputs,tools=TOOLS,tool_choice="auto")
        answer=r.output_text or "Ich leite das an unser Team weiter."
    db.add(Message(conversation_id=conversation.id, role="assistant", content=answer)); await db.commit()
    return answer
