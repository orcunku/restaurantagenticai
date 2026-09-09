from fastapi import APIRouter
from pydantic import BaseModel

from app.demo_data import RESTAURANTS, dashboard_payload, demo_reply

router = APIRouter(prefix="/demo", tags=["synthetic-demo"])

class DemoChatIn(BaseModel):
    message: str

@router.get("/dashboard/{slug}")
async def demo_dashboard(slug: str):
    return dashboard_payload(slug)

@router.get("/restaurants")
async def demo_restaurants():
    return [{"slug": slug, **data} for slug, data in RESTAURANTS.items()]

@router.post("/chat/{slug}")
async def synthetic_chat(slug: str, body: DemoChatIn):
    return demo_reply(slug, body.message)
