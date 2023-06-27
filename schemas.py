from typing import Optional, List
from pydantic import BaseModel


class AirConditioner(BaseModel):
    id: Optional[str] = None
    model: str
    temperature: Optional[float] = None
    room_id: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateAirConditioner(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    room_id: Optional[str] = None


class Room(BaseModel):
    id: Optional[str] = None
    name: str
    sensor: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_conditioners: Optional[List[AirConditioner]] = None

    class Config:
        orm_mode = True


class UpdateRoom(BaseModel):
    name: Optional[str] = None
    sensor: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_conditioners: Optional[List[AirConditioner]] = None
