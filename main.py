from fastapi import FastAPI
from models.settings import Settings
#from models.db import Sensor, SensorSchema, generate_token, Base, Event, EventSchema, EventType, EventTypeSchema
from models.db import EventSchema, Event, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from management import manage

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
    return {"message": "Event added successfully", "event_id": new_event.IDEvent}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8801, reload=True)
