from sqlalchemy import text, select
from app.db.session import engine, SessionLocal
from app.db.models import Base, Restaurant, KnowledgeChunk
from app.core.config import get_settings
from app.services.rag import embed_text

DEMO_KNOWLEDGE = [
    ("hours","Öffnungszeiten","Montag bis Samstag 11:30–23:00. Küche bis 22:00. Sonntag geschlossen."),
    ("menu","Speisekarte","Wiener Schnitzel €24, Kürbisrisotto vegan €19, Forelle €27. Glutenfreie Pasta ist auf Anfrage verfügbar."),
    ("allergens","Allergene","Glutenfreie Optionen sind verfügbar. Bei schweren Allergien muss das Serviceteam bestätigen; der Assistent darf keine Sicherheitsgarantie geben."),
    ("policies","Reservierung","Terrasse nach Verfügbarkeit. Gruppen ab 8 Personen bitte an das Team eskalieren. Hunde sind willkommen. Kinderstühle vorhanden."),
    ("location","Anreise","Demo Bistro, Ringstraße 1, 1010 Wien. U-Bahn Station Karlsplatz, 5 Minuten zu Fuß."),
]

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    settings = get_settings()
    async with SessionLocal() as db:
        existing = (await db.execute(select(Restaurant).where(Restaurant.slug==settings.demo_restaurant_slug))).scalar_one_or_none()
        if existing: return
        r = Restaurant(slug=settings.demo_restaurant_slug, name="Demo Bistro Wien")
        db.add(r); await db.flush()
        for kind,title,content in DEMO_KNOWLEDGE:
            emb = await embed_text(content)
            db.add(KnowledgeChunk(restaurant_id=r.id, kind=kind, title=title, content=content, embedding=emb))
        await db.commit()
