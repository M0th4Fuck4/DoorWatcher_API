from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer, create_engine, ForeignKey, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker
from models.settings import Settings
from typing import List
import secrets, string
from datetime import datetime

settings = Settings()

def generate_token() -> str:
    unique = False
    alphabet = string.ascii_uppercase + string.digits
    while not unique:
        token = ''.join(secrets.choice(alphabet) for i in range(5)) + "-" + ''.join(secrets.choice(alphabet) for i in range(5)) + "-" + ''.join(secrets.choice(alphabet) for i in range(5)) + "-" + ''.join(secrets.choice(alphabet) for i in range(5))
        engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        sensor = session.query(Sensor).filter(and_(Sensor.Active == True, Sensor.SensorKey == token)).all()
        if len(sensor) == 0:
            unique = True
    return token

def sensor_exist(token) -> bool:
    engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    sensor = session.query(Sensor).filter(and_(Sensor.Active == True, Sensor.SensorKey == token)).all()
    if len(sensor) == 0:
        return False
    else:
        return True

# --- SQLAlchemy 2.0 Model ---
class Base(DeclarativeBase):
    pass

class Sensor(Base):
    __tablename__ = "t-sensors"

    IDSensor: Mapped[int] = mapped_column(primary_key=True)
    SensorKey: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
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
    SensorKey: Mapped[Sensor] = mapped_column(ForeignKey("t-sensors.SensorKey"), nullable=False)
    Type: Mapped[EventType] = mapped_column(ForeignKey("t-event-types.EventTypeName"), nullable=False)
    EventTimestamp: Mapped[str] = mapped_column(String(50), nullable=False, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

class Videos(Base):
    __tablename__ = "t-videos"

    IDVideo: Mapped[int] = mapped_column(primary_key=True)
    IDEvent: Mapped[Event] = mapped_column(ForeignKey("t-events.IDEvent"), nullable=False)
    Path: Mapped[str] = mapped_column(String(255), nullable=False)

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
