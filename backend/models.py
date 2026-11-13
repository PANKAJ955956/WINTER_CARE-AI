from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Screening(Base):
    __tablename__ = "screenings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    age: Mapped[int] = mapped_column(Integer)
    temperature_c: Mapped[float] = mapped_column(Float, default=36.8)
    symptoms: Mapped[str] = mapped_column(Text, default="")
    risk_conditions: Mapped[str] = mapped_column(Text, default="")
    breathing_difficulty: Mapped[bool] = mapped_column(Boolean, default=False)
    chest_pain: Mapped[bool] = mapped_column(Boolean, default=False)
    confusion: Mapped[bool] = mapped_column(Boolean, default=False)
    duration_days: Mapped[int] = mapped_column(Integer, default=1)
    risk_score: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(20))
    factors: Mapped[str] = mapped_column(Text, default="")
    recommendation: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class HealthEvent(Base):
    __tablename__ = "health_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    location: Mapped[str] = mapped_column(String(200))
    event_date: Mapped[str] = mapped_column(String(30))
    expected_attendance: Mapped[int] = mapped_column(Integer, default=100)
    cold_exposure: Mapped[str] = mapped_column(String(30), default="moderate")
    first_aid_posts: Mapped[int] = mapped_column(Integer, default=1)
    staff_count: Mapped[int] = mapped_column(Integer, default=2)
    readiness_score: Mapped[int] = mapped_column(Integer, default=50)
    checklist: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class InventoryItem(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String(120), unique=True)
    category: Mapped[str] = mapped_column(String(80), default="First aid")
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    minimum_quantity: Mapped[int] = mapped_column(Integer, default=5)
    unit: Mapped[str] = mapped_column(String(30), default="units")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_name: Mapped[str] = mapped_column(String(160))
    incident_type: Mapped[str] = mapped_column(String(100))
    severity: Mapped[str] = mapped_column(String(30), default="moderate")
    description: Mapped[str] = mapped_column(Text, default="")
    action_taken: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
