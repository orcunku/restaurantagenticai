from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.init_db import init_db
from app.api.routes import router as api_router
from app.api.twilio_routes import router as twilio_router
from app.api.demo_routes import router as demo_router
from app.core.config import get_settings

@asynccontextmanager
async def lifespan(app):
    await init_db(); yield

app=FastAPI(title="EU Restaurant AI Frontdesk",version="0.1.0",lifespan=lifespan)
app.include_router(api_router,prefix="/api")
app.include_router(twilio_router)
app.include_router(demo_router)
app.mount("/static",StaticFiles(directory="app/static"),name="static")
templates=Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"slug":"vienna-table"})
