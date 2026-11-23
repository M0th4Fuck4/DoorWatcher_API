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

@router.get("/generate-token/")
def generate_token_endpoint():
    return {"token": generate_token()}

@router.get("/sensors/list/")
def get_sensors():
    session = Session()
    sensors = session.query(Sensor).filter(Sensor.Active == True).all()
    session.close()
    return {"sensors": [SensorSchema.from_orm(sensor) for sensor in sensors]}

@router.post("/sensors/add/")
def add_sensor(sensor: SensorSchema):
    session = Session()
    new_sensor = Sensor(
        SensorKey=sensor.SensorKey,
        SensorName=sensor.SensorName,
        SensorType=sensor.SensorType,
        SensorLocation=sensor.SensorLocation,
        Active=sensor.Active
    )
    session.add(new_sensor)
    session.commit()
    session.refresh(new_sensor)
    session.close()
    return {"message": "Sensor added successfully", "sensor_id": new_sensor.IDSensor}

@router.post("/sensors/deactivate/{sensor_id}")
def deactivate_sensor(sensor_id: int):
    session = Session()
    sensor = session.query(Sensor).filter(Sensor.IDSensor == sensor_id).first()
    if sensor:
        sensor.Active = False
        session.commit()
        session.close()
        return {"message": "Sensor deactivated successfully"}
    else:
        session.close()
        return {"message": "Sensor not found"}

@router.post("/sensors/activate/{sensor_id}")
def activate_sensor(sensor_id: int):
    session = Session()
    sensor = session.query(Sensor).filter(Sensor.IDSensor == sensor_id).first()
    if sensor:
        sensor.Active = True
        session.commit()
        session.close()
        return {"message": "Sensor activated successfully"}
    else:
        session.close()
        return {"message": "Sensor not found"}
