from fastapi import APIRouter
from models.settings import Settings
from models.db import Subscribers, SubscriberSchema, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()

engine = create_engine(settings.get_settings().get("DB_TYPE")+"://"+settings.get_settings().get("DB_USER")+":"+settings.get_settings().get("DB_PASSWORD")+"@"+settings.get_settings().get("DB_HOST")+":"+str(settings.get_settings().get("DB_PORT"))+"/"+settings.get_settings().get("DB_NAME"), echo=False)
Session = sessionmaker(bind=engine)

# Initialize the router
router = APIRouter()

@router.get("/subscribers/list/")
def get_subscribers():
    session = Session()
    subscribers = session.query(Subscribers).filter(Subscribers.Active == True).all()
    session.close()
    return {"subscribers": [SubscriberSchema.from_orm(subscriber) for subscriber in subscribers]}

@router.post("/subscribers/add/")
def add_subscriber(subscriber: SubscriberSchema):
    session = Session()
    new_subscriber = Subscribers(
        SubscriberName=subscriber.SubscriberName,
        SubscriberCell=subscriber.SubscriberCell,
        Active=subscriber.Active
    )
    session.add(new_subscriber)
    session.commit()
    session.refresh(new_subscriber)
    session.close()
    return {"message": "Subscriber added successfully", "subscriber_id": new_subscriber.IDSubscriber}

@router.post("/subscribers/deactivate/{subscriber_id}")
def deactivate_subscriber(subscriber_id: int):
    session = Session()
    subscriber = session.query(Subscribers).filter(Subscribers.IDSubscriber == subscriber_id).first()
    if subscriber:
        subscriber.Active = False
        session.commit()
        session.close()
        return {"message": "Subscriber deactivated successfully"}
    else:
        session.close()
        return {"message": "Subscriber not found"}

@router.post("/subscribers/activate/{subscriber_id}")
def activate_subscriber(subscriber_id: int):
    session = Session()
    subscriber = session.query(Subscribers).filter(Subscribers.IDSubscriber == subscriber_id).first()
    if subscriber:
        subscriber.Active = True
        session.commit()
        session.close()
        return {"message": "Subscriber activated successfully"}
    else:
        session.close()
        return {"message": "Subscriber not found"}
