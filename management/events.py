from fastapi import APIRouter
from models.settings import Settings
from models.db import Sensor, SensorSchema, generate_token, Base, Event, EventSchema, EventType, EventTypeSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()

engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=False)
Session = sessionmaker(bind=engine)

# Initialize the router
router = APIRouter()

@router.get("/events-types/list/")
def get_event_types():
    session = Session()
    event_types = session.query(EventType).filter(EventType.Active == True).all()
    session.close()
    return {"event_types": [EventTypeSchema.from_orm(event_type) for event_type in event_types]}

@router.post("/events-types/add/")
def add_event_type(event_type: EventTypeSchema):
    session = Session()
    new_event_type = EventType(
        EventTypeName=event_type.EventTypeName,
        EventDescription=event_type.EventDescription,
        Active=event_type.Active
    )
    session.add(new_event_type)
    session.commit()
    session.refresh(new_event_type)
    session.close()
    return {"message": "Event type added successfully", "event_type_id": new_event_type.IDEventType}

@router.post("/events-types/deactivate/{event_type_id}")
def deactivate_event_type(event_type_id: int):
    session = Session()
    event_type = session.query(EventType).filter(EventType.IDEventType == event_type_id).first()
    if event_type:
        event_type.Active = False
        session.commit()
        session.close()
        return {"message": "Event type deactivated successfully"}
    else:
        session.close()
        return {"message": "Event type not found"}

@router.post("/events-types/activate/{event_type_id}")
def activate_event_type(event_type_id: int):
    session = Session()
    event_type = session.query(EventType).filter(EventType.IDEventType == event_type_id).first()
    if event_type:
        event_type.Active = True
        session.commit()
        session.close()
        return {"message": "Event type activated successfully"}
    else:
        session.close()
        return {"message": "Event type not found"}
