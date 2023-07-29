import asyncio
from fastapi import FastAPI, Depends, Query,BackgroundTasks
from fastapi_pagination import Page
from app.schemas import CarFilter, CarFilterSchema, CarSchema
from .database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct
from .models import Car
from fastapi_pagination import add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
import nats

app = FastAPI()
# Fast API Pagination initilization
add_pagination(app)

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure NATS
NATS_SERVERS = ["nats://0.0.0.0:4222"]
NATS_SUBJECT = "test.fatstapi"


async def subscribe_to_nats_subject():
    nc = await nats.connect("demo.nats.io")
    js = nc.jetstream()

    try:
        # Persist messages on 'foo's subject.
        # await js.add_stream(name="fastapi-sample-stream", subjects=["akfastapi.cars"])

        # for i in range(0, 1):
        #     ack = await js.publish("akfastapi.cars", f"hello world: {i}".encode())
        #     print(ack)
 
        # Create pull based consumer on 'foo'.
        psub = await js.pull_subscribe("akfastapi.cars", "psub-ak-fastapi")
        print("Subscribed to NATS subject.")

        # Fetch and ack messagess from consumer.
        while True:
            try:
                msgs = await psub.fetch(1000,timeout=1)
                for msg in msgs:
                    await msg.ack()
                    # print(msg)
                    print(f"Received message: {msg.data.decode()}")
            except Exception as e:
                psub = await js.pull_subscribe("akfastapi.cars", "psub-ak-fastapi")

    except Exception as e:
        print(f"Error in NATS subscription: {e}")

    finally:
        # Close the NATS connection when the app is shut down
        await nc.close()
        print(f"nats connection closed")



    
@app.on_event("startup")
async def startup_event():
    # Start subscribing to the NATS subject on app startup
    app.state.nats_subscription_task = asyncio.create_task(subscribe_to_nats_subject())
    print("finished nats start up")

@app.on_event("shutdown")
async def shutdown_event():
    # Cancel the NATS subscription task on app shutdown
    print("shutting-down app")
    app.state.nats_subscription_task.cancel()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/cars", response_model=Page[CarSchema])
async def get_all_paginated_cars(db_session: Session = Depends(get_db)):
    return paginate(db_session, select(Car))


@app.get("/car/filters", response_model=Page[CarFilterSchema])
async def get_column_filters_for_car(
    filter_list: CarFilter = Query(
        ...,
        description="provide the attribute of the column you want to filter result, takes attriburte as name or brand",
    ),
    db_session: Session = Depends(get_db),
):

    if filter_list == "brand":
        return paginate(
            db_session,
            select(distinct(Car.brand)),
            transformer=lambda items: [{"brand": brand} for brand in items],
        )
    else:
        return paginate(
            db_session,
            select(Car.name),
            transformer=lambda items: [{"name": name} for name in items],
        )
