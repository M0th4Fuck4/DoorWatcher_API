from fastapi import FastAPI, BackgroundTasks
from models.settings import Settings
from models.db import EventSchema, SensorSchema, Event, Base, generate_token, sensor_exist, Sensor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from management import manage
import requests, time, asyncio

settings = Settings()

SHINOBI_URL = settings.get_settings().get("SHINOBI_HOST") + ":" + settings.get_settings().get("SHINOBI_PORT")
SHINOBI_START = SHINOBI_URL + "/" + settings.get_settings().get("SHINOBI_API_KEY") + "/monitor/" + settings.get_settings().get("SHINOBI_GROUP_KEY") + "/" + settings.get_settings().get("SHINOBI_MONITOR_ID") + "/record"
SHINOBI_STOP = SHINOBI_URL + "/" + settings.get_settings().get("SHINOBI_API_KEY") + "/monitor/" + settings.get_settings().get("SHINOBI_GROUP_KEY") + "/" + settings.get_settings().get("SHINOBI_MONITOR_ID") + "/stop"
SHINOBI_LIST_VIDEO = SHINOBI_URL + "/" + settings.get_settings().get("SHINOBI_API_KEY") + "/videos/" + settings.get_settings().get("SHINOBI_GROUP_KEY") + "/" + settings.get_settings().get("SHINOBI_MONITOR_ID")

engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI(root_path="/DoorWatcherApi")
app.include_router(manage.router)

@app.post("/events/add/")
async def add_event(event: EventSchema, background_tasks: BackgroundTasks):
    session = Session()
    if not sensor_exist(event.sKey):
        new_sensor = Sensor(
        SensorKey=event.sKey,
        SensorName=event.sName,
        SensorType=event.sType,
        SensorLocation=event.sLocation,
        Active=1)
        session.add(new_sensor)
        session.commit()
        session.refresh(new_sensor)

    new_event = Event(
        SensorKey = event.sKey,
        Type = event.sAction
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    if event.sAction == "Open":
        background_tasks.add_task(recording)
    return {"message": "Event added successfully", "event_id": new_event.IDEvent}

async def recording():
    print("Start recording...")
    response = requests.get(SHINOBI_START)
    print(response.text)
    response = requests.get(SHINOBI_LIST_VIDEO)
    print(response.text)
    await asyncio.sleep(1)
    response = requests.get(SHINOBI_STOP)
    print(response.text)
    print("Stop recording...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.get_settings().get("DOORWATCHER_PORT"), reload=True)
