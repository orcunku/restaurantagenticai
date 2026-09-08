import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Boolean, JSON, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase): pass

def uid(): return str(uuid.uuid4())

class Restaurant(Base):
    __tablename__ = "restaurants"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    timezone: Mapped[str] = mapped_column(String, default="Europe/Vienna")
    default_language: Mapped[str] = mapped_column(String, default="de-AT")
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    reservation_provider: Mapped[str] = mapped_column(String, default="mock")
    reservation_config: Mapped[dict] = mapped_column(JSON, default=dict)
    pos_provider: Mapped[str] = mapped_column(String, default="none")
    pos_config: Mapped[dict] = mapped_column(JSON, default=dict)
    ai_disclosure: Mapped[str] = mapped_column(String, default="Sie sprechen mit dem digitalen Assistenten unseres Restaurants.")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    restaurant_id: Mapped[str] = mapped_column(ForeignKey("restaurants.id"), index=True)
    kind: Mapped[str] = mapped_column(String, default="general")
    title: Mapped[str] = mapped_column(String, default="")
    content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    restaurant_id: Mapped[str] = mapped_column(ForeignKey("restaurants.id"), index=True)
    channel: Mapped[str] = mapped_column(String)
    external_user_id: Mapped[str] = mapped_column(String, index=True)
    external_session_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"), index=True)
    role: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Reservation(Base):
    __tablename__ = "reservations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    restaurant_id: Mapped[str] = mapped_column(ForeignKey("restaurants.id"), index=True)
    provider_id: Mapped[str | None] = mapped_column(String, nullable=True)
    guest_name: Mapped[str] = mapped_column(String)
    guest_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    guest_email: Mapped[str | None] = mapped_column(String, nullable=True)
    party_size: Mapped[int] = mapped_column(Integer)
    start_at: Mapped[datetime] = mapped_column(DateTime)
    seating: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="confirmed")
    estimated_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
