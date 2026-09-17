from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from models.settings import Settings
from typing import List
import secrets
from datetime import datetime

settings = Settings()

def generate_token() -> str:
    return secrets.token_hex(16)

# --- SQLAlchemy 2.0 Model ---
class Base(DeclarativeBase):
    pass

class Sensor(Base):
    __tablename__ = "t-sensors"

    IDSensor: Mapped[int] = mapped_column(primary_key=True)
    SensorKey: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, default=generate_token())
    SensorName: Mapped[str] = mapped_column(String(50))
    SensorType: Mapped[str] = mapped_column(String(50))
    SensorLocation: Mapped[str] = mapped_column(String(50))
    Active: Mapped[bool] = mapped_column(default=True)

class EventType(Base):
    __tablename__ = "t-event-types"

    IDEventType: Mapped[int] = mapped_column(primary_key=True)
    EventTypeName: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    Active: Mapped[bool] = mapped_column(default=True)

class Event(Base):
    __tablename__ = "t-events"

    IDEvent: Mapped[int] = mapped_column(primary_key=True)
    #SensorKey: Mapped[str] = mapped_column(String(50), nullable=False)
    SensorKey: Mapped[Sensor] = mapped_column(ForeignKey("t-sensors.SensorKey"), nullable=False)
    #EventType: Mapped[int] = mapped_column(Integer, nullable=False)
    Type: Mapped[EventType] = mapped_column(ForeignKey("t-event-types.EventTypeName"), nullable=False)
    EventTimestamp: Mapped[str] = mapped_column(String(50), nullable=False, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

# --- Pydantic v2 Schema ---
class SensorSchema(BaseModel):
    SensorKey: str
    SensorName: str
    SensorType: str
    SensorLocation: str
    Active: bool

    model_config = ConfigDict(from_attributes=True)

class EventSchema(BaseModel):
    sKey: str
    sName: str
    sType: str
    sLocation: str
    sAction: str
    sPourcentage: int

    model_config = ConfigDict(from_attributes=True)

class EventTypeSchema(BaseModel):
    EventTypeName: str
    Active: bool

    model_config = ConfigDict(from_attributes=True)
