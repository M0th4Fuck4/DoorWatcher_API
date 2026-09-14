from fastapi import APIRouter
from models.settings import Settings
from models.db import Sensor, SensorSchema, generate_token, Base, Event, EventSchema, EventType, EventTypeSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()

engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=True)
Session = sessionmaker(bind=engine)

# Initialize the router
router = APIRouter()

@router.get("/generate-token")
def generate_token_endpoint():
    return {"token": generate_token()}

@router.get("/events-types/list/")
def get_event_types():
    session = Session()
    event_types = session.query(EventType).filter(EventType.Active == True).all()
    session.close()
    return {"event_types": [EventTypeSchema.from_orm(event_type) for event_type in event_types]}

@router.get("/sensors/list/")
def get_sensors():
    session = Session()
    sensors = session.query(Sensor).filter(Sensor.Active == True).all()
    session.close()
    return {"sensors": [SensorSchema.from_orm(sensor) for sensor in sensors]}

@router.post("/sensors/add/")
def create_sensor(sensor: SensorSchema):
    session = Session()
    new_sensor = Sensor(
        SensorKey=sensor.SensorKey,
        SensorName=sensor.SensorName,
        SensorType=sensor.SensorType,
        SensorLocation=sensor.SensorLocation,
        Active=sensor.Active
    )
    try:
        session.add(new_sensor)
        session.commit()
        session.refresh(new_sensor)
    except Exception as e:
        session.rollback()
        return {"message": "Sensor creation failed", "error": str(e)}
    finally:
        session.close()

    return {"message": "Sensor added successfully", "sensor_id": new_sensor.IDSensor, "sensor_key": new_sensor.SensorKey}

@router.post("/event-types/add/")
def create_event_type(event_type: EventTypeSchema):
    session = Session()
    new_event_type = EventType(
        EventTypeName=event_type.EventTypeName,
        Active=event_type.Active
    )
    session.add(new_event_type)
    session.commit()
    session.refresh(new_event_type)
    session.close()
    return {"message": "Event type added successfully", "event_type_id": new_event_type.IDEventType}
