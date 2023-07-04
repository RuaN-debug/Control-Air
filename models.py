from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RoomDb(Base):
    __tablename__ = 'room'

    id = Column(String, primary_key=True, index=True, nullable=True)
    name = Column(String, index=True)
    sensor = Column(String)
    temperature = Column(Float, default=0)
    humidity = Column(Float, default=0)
    air_conditioners = relationship("AirConditionerDb", back_populates="room")

    def __repr__(self):
        return f"{self.name}"


class AirConditionerDb(Base):
    __tablename__ = 'air_conditioner'

    id = Column(String, primary_key=True, index=True, nullable=True)
    model = Column(String, index=True)
    temperature = Column(Float, default=22)
    room_id = Column(String, ForeignKey('room.id'))
    room = relationship("RoomDb", back_populates="air_conditioners")

    def __repr__(self):
        return f"{self.model}"
