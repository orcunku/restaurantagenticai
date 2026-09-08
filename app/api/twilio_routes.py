from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy import select
from twilio.request_validator import RequestValidator
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from app.db.session import get_db
from app.db.models import Restaurant
from app.core.config import get_settings
from app.services.agent import get_or_create_conversation, run_agent

router=APIRouter(prefix="/webhooks/twilio"); settings=get_settings()

async def restaurant_for_request(db, request):
    slug=request.query_params.get("restaurant",settings.demo_restaurant_slug)
    r=(await db.execute(select(Restaurant).where(Restaurant.slug==slug))).scalar_one_or_none()
    if not r: raise HTTPException(404,"Restaurant not found")
    return r

def validate_twilio(request:Request, form:dict):
    if not settings.twilio_auth_token or settings.app_env=="development": return
    signature=request.headers.get("X-Twilio-Signature","")
    if not RequestValidator(settings.twilio_auth_token).validate(str(request.url),form,signature): raise HTTPException(403,"Invalid Twilio signature")

@router.post("/whatsapp")
async def whatsapp(request:Request,db=Depends(get_db)):
    form=dict(await request.form()); validate_twilio(request,form); r=await restaurant_for_request(db,request)
    sender=form.get("From","unknown"); text=form.get("Body",""); c=await get_or_create_conversation(db,r.id,"whatsapp",sender)
    answer=await run_agent(db,r,c,text); resp=MessagingResponse(); resp.message(answer); return Response(str(resp),media_type="application/xml")

@router.post("/voice/incoming")
async def voice_incoming(request:Request,db=Depends(get_db)):
    form=dict(await request.form()); validate_twilio(request,form); r=await restaurant_for_request(db,request)
    vr=VoiceResponse(); vr.say(r.ai_disclosure,language="de-DE")
    g=Gather(input="speech",action=f"/webhooks/twilio/voice/gather?restaurant={r.slug}",method="POST",language="de-DE",speech_timeout="auto",action_on_empty_result=True)
    g.say(f"Willkommen bei {r.name}. Wie kann ich Ihnen helfen?",language="de-DE"); vr.append(g)
    return Response(str(vr),media_type="application/xml")

@router.post("/voice/gather")
async def voice_gather(request:Request,db=Depends(get_db)):
    form=dict(await request.form()); validate_twilio(request,form); r=await restaurant_for_request(db,request)
    call_sid=form.get("CallSid","unknown"); caller=form.get("From","unknown"); text=form.get("SpeechResult","").strip()
    vr=VoiceResponse()
    if not text: vr.say("Ich habe Sie leider nicht verstanden. Auf Wiederhören.",language="de-DE"); return Response(str(vr),media_type="application/xml")
    c=await get_or_create_conversation(db,r.id,"voice",caller,call_sid); answer=await run_agent(db,r,c,text)
    g=Gather(input="speech",action=f"/webhooks/twilio/voice/gather?restaurant={r.slug}",method="POST",language="de-DE",speech_timeout="auto",action_on_empty_result=True)
    g.say(answer,language="de-DE"); g.say("Kann ich sonst noch etwas für Sie tun?",language="de-DE"); vr.append(g)
    return Response(str(vr),media_type="application/xml")
