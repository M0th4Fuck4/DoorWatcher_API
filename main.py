from fastapi import FastAPI
from models.settings import Settings
#from models.db import Sensor, SensorSchema, generate_token, Base, Event, EventSchema, EventType, EventTypeSchema
from models.db import EventSchema, Event, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from management import manage
import requests, time

settings = Settings()

engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI(root_path="/DoorWatcherApi")
app.include_router(manage.router)

@app.post("/events/add/")
def create_event(event: EventSchema):
    session = Session()
    new_event = Event(
        SensorKey=event.SensorKey,
        Type=event.Type
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    session.close()
    if new_event.Type == "Ouverture":
        SHINOBI_URL = settings.get_settings().get("SHINOBI_HOST") + ":" + settings.get_settings().get("SHINOBI_PORT")
        SHINOBI_START = SHINOBI_URL + "/" + settings.get_settings().get("SHINOBI_API_KEY") + "/monitor/" + settings.get_settings().get("SHINOBI_GROUP_KEY") + "/" + settings.get_settings().get("SHINOBI_MONITOR_ID") + "/record"
        SHINOBI_STOP = SHINOBI_URL + "/" + settings.get_settings().get("SHINOBI_API_KEY") + "/monitor/" + settings.get_settings().get("SHINOBI_GROUP_KEY") + "/" + settings.get_settings().get("SHINOBI_MONITOR_ID") + "/stop"
        print(SHINOBI_START)
        response_start = requests.get(SHINOBI_START)
        if response_start.status_code == 200:
            print("Recording for " + str(settings.get_settings().get("SHINOBI_DURATION")) +" seconds")
            time.sleep(settings.get_settings().get("SHINOBI_DURATION"))
            response_stop = requests.get(SHINOBI_STOP)
            print("Stopping record")
            print(response_stop.status_code)
        else:
            print("Failed to start recording. Status: " + str(response_start.status_code))
    return {"message": "Event added successfully", "event_id": new_event.IDEvent}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8801, reload=True)
