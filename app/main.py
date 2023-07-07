from typing import Union
from fastapi import FastAPI, Depends, Query
from fastapi_pagination import Page
from app.schemas import CarFilter, CarFilterSchema, CarSchema
from .database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct
from .models import Car
from fastapi_pagination import add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

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
        stmt = select(Car).distinct(Car.brand)
        return paginate(
            db_session, stmt
        )  # This result is invalid , as i require only unique car brand names in the db
    else:
        return paginate(db_session, select(Car.name))
