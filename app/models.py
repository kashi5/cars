from sqlalchemy import  Column, Integer, String


from .database import Base


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
