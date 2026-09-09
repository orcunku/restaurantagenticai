from openai import AsyncOpenAI
from sqlalchemy import select

from app.core.config import get_settings
from app.db.models import KnowledgeChunk

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

async def embed_text(text: str) -> list[float] | None:
    if not client: return None
    r = await client.embeddings.create(model=settings.openai_embedding_model, input=text)
    return r.data[0].embedding

async def search_knowledge(db, restaurant_id: str, query: str, limit: int = 5):
    qemb = await embed_text(query)
    if qemb:
        stmt = (select(KnowledgeChunk)
                .where(KnowledgeChunk.restaurant_id==restaurant_id)
                .order_by(KnowledgeChunk.embedding.cosine_distance(qemb))
                .limit(limit))
    else:
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.restaurant_id==restaurant_id).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return [{"kind":x.kind,"title":x.title,"content":x.content,"metadata":x.metadata_json} for x in rows]
