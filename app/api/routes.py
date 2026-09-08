from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select, func
from app.db.session import get_db
from app.db.models import Restaurant, KnowledgeChunk, Reservation, Conversation, Message
from app.api.schemas import RestaurantCreate, KnowledgeIn, ChatIn
from app.services.rag import embed_text
from app.services.agent import get_or_create_conversation, run_agent
from app.core.config import get_settings

router=APIRouter(); settings=get_settings()

def admin_guard(x_admin_key: str|None=Header(default=None)):
    if x_admin_key!=settings.admin_api_key: raise HTTPException(401,"Invalid admin key")

async def restaurant_by_slug(db,slug):
    r=(await db.execute(select(Restaurant).where(Restaurant.slug==slug,Restaurant.active==True))).scalar_one_or_none()
    if not r: raise HTTPException(404,"Restaurant not found")
    return r

@router.get("/health")
async def health(): return {"ok":True}

@router.post("/admin/restaurants",dependencies=[Depends(admin_guard)])
async def create_restaurant(body:RestaurantCreate,db=Depends(get_db)):
    r=Restaurant(**body.model_dump()); db.add(r); await db.commit(); await db.refresh(r); return {"id":r.id,"slug":r.slug}

@router.post("/admin/restaurants/{slug}/knowledge",dependencies=[Depends(admin_guard)])
async def add_knowledge(slug:str,body:KnowledgeIn,db=Depends(get_db)):
    r=await restaurant_by_slug(db,slug); emb=await embed_text(body.content)
    x=KnowledgeChunk(restaurant_id=r.id,kind=body.kind,title=body.title,content=body.content,metadata_json=body.metadata,embedding=emb); db.add(x); await db.commit(); return {"id":x.id}

@router.get("/admin/restaurants/{slug}/metrics",dependencies=[Depends(admin_guard)])
async def metrics(slug:str,db=Depends(get_db)):
    r=await restaurant_by_slug(db,slug)
    reservations=(await db.execute(select(func.count()).select_from(Reservation).where(Reservation.restaurant_id==r.id))).scalar_one()
    conversations=(await db.execute(select(func.count()).select_from(Conversation).where(Conversation.restaurant_id==r.id))).scalar_one()
    return {"restaurant":r.name,"reservations":reservations,"conversations":conversations}

@router.post("/chat/{slug}")
async def chat(slug:str,body:ChatIn,db=Depends(get_db)):
    r=await restaurant_by_slug(db,slug); c=await get_or_create_conversation(db,r.id,"web",body.user_id,body.session_id)
    return {"reply":await run_agent(db,r,c,body.message),"conversation_id":c.id}
