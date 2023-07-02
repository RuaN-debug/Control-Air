from schemas import (
    Room,
    UpdateRoom,
    AirConditioner,
    UpdateAirConditioner
)
from models import AirConditionerDb as air_conditioner_db
from models import RoomDb as room_db
from utils import room_dict_response
from sqlalchemy.orm import Session
from uuid import uuid4 as uuid


# Cômodo
def retrieve_all_rooms(db):
    rooms = db.query(room_db).all()
    if rooms:
        rooms_dict = [room_dict_response(
            room, room.air_conditioners) for room in rooms]
        return rooms_dict

    return rooms


def retrieve_room(room_id: str, db: Session):
    room = db.query(room_db).filter(room_db.id == room_id).one_or_none()
    if room:
        room_dict = room_dict_response(room, room.air_conditioners)
        return room_dict

    return room


def create_room(room: Room, db: Session):
    if not room.id:
        room.id = str(uuid())

    if retrieve_room(room.id, db):
        return None

    new_air_conditioners = []
    for air_conditioner in room.air_conditioners:
        new_air_conditioner = create_air_conditioner(air_conditioner, db)
        new_air_conditioners.append(new_air_conditioner)

    room.air_conditioners = new_air_conditioners
    new_room = room_db(**room.dict())
    db.add(new_room)
    db.commit()

    return new_room


def remove_room(room_id: str, db: Session):
    room = db.query(room_db).filter(room_db.id == room_id).one_or_none()
    if not room:
        return None

    if room.air_conditioners:
        for air_conditioner in room.air_conditioners:
            remove_air_conditioner(air_conditioner.id, db)
            
    db.delete(room)
    db.commit()

    return room


def change_room(room_id: str, new_room: UpdateRoom, db: Session):
    room = db.query(room_db).filter(room_db.id == room_id).one_or_none()
    if not room:
        return None

    air_conditioner = None
    if new_room.air_conditioners:
        air_conditioner = new_room.air_conditioners[0]
        new_room.air_conditioners = None
        
    if air_conditioner:
        room.air_conditioners[0].model = air_conditioner.model
        
    for item, value in vars(new_room).items():
        setattr(room, item, value) if value else None

    db.commit()
    db.refresh(room)

    return room


# Ar condicionado
def retrieve_all_air_conditioners(db):
    return db.query(air_conditioner_db).all()


def retrieve_air_conditioner(air_conditioner_id: str, db: Session):
    return db.query(air_conditioner_db).filter(air_conditioner_db.id == air_conditioner_id).one_or_none()


def create_air_conditioner(air_conditioner: AirConditioner, db: Session):
    if not air_conditioner.id:
        air_conditioner.id = str(uuid())

    new_air_conditioner = air_conditioner_db(**air_conditioner.dict())
    if retrieve_air_conditioner(air_conditioner.id, db):
        return None

    db.add(new_air_conditioner)
    db.commit()

    return new_air_conditioner


def remove_air_conditioner(air_conditioner_id: str, db: Session):
    air_conditioner = retrieve_air_conditioner(air_conditioner_id, db)
    if not air_conditioner:
        return None

    db.delete(air_conditioner)
    db.commit()

    return air_conditioner


def change_air_conditioner(air_conditioner_id: str, new_air_conditioner: UpdateAirConditioner, db: Session):
    air_conditioner = retrieve_air_conditioner(air_conditioner_id, db)
    if not air_conditioner:
        return None

    for item, value in vars(new_air_conditioner).items():
        setattr(air_conditioner, item, value) if value else None

    db.commit()
    db.refresh(air_conditioner)

    return air_conditioner
