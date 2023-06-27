from schemas import Room, UpdateRoom, AirConditioner, UpdateAirConditioner
from fastapi import FastAPI, HTTPException, WebSocket, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from database import database
from database import engine
from crud import (
    retrieve_all_rooms,
    retrieve_room,
    create_room,
    remove_room,
    change_room,
    retrieve_all_air_conditioners,
    retrieve_air_conditioner,
    create_air_conditioner,
    remove_air_conditioner,
    change_air_conditioner
)

import models


app = FastAPI(
    title="Control Air",
    description="API para controle de ar condicionado",
    version="0.0.1",
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")


# Redireciona para o docs
@app.get("/")
async def main():
    return RedirectResponse(url="/docs/")


# Rota get todos os cômodos
@app.get("/get-rooms")
async def get_all_rooms(db: Session = Depends(get_db)):
    rooms = retrieve_all_rooms(db)
    if not rooms:
        return HTTPException(status_code=404, detail="Rooms not found")

    return rooms


# Rota get cômodo por id
@app.get("/get-room/{room_id}")
async def get_room(room_id: str, db: Session = Depends(get_db)):
    room = retrieve_room(room_id, db)
    if not room:
        return HTTPException(status_code=404, detail="Room not found")

    return room


# Rota inserir cômodo
@app.post("/create-room")
async def post_room(room: Room, db: Session = Depends(get_db)):
    room = create_room(room, db)
    if not room:
        return HTTPException(status_code=404, detail="Room not created")

    return {"Message": f"Room '{room}' created successfully"}


# Rota deletar cômodo
@app.delete("/delete-room/{room_id}")
async def delete_room(room_id: str, db: Session = Depends(get_db)):
    room = remove_room(room_id, db)
    if not room:
        return HTTPException(status_code=404, detail="Room not deleted")

    return {"Message": f"Room '{room}' deleted successfully"}


# Rota atualizar cômodo
@app.put("/update-room/{room_id}")
async def update_room(room_id: str, new_room: UpdateRoom, db: Session = Depends(get_db)):
    room = change_room(room_id, new_room, db)
    if not room:
        return HTTPException(status_code=404, detail="Room not updated")

    return {"Message": f"Room '{room}' updated successfully"}


# Rota get todos os ar-condicionados
@app.get("/get-air-conditioners")
async def get_all_air_conditioners(db: Session = Depends(get_db)):
    air_conditioners = retrieve_all_air_conditioners(db)
    if not air_conditioners:
        return HTTPException(status_code=404, detail="Air Conditioners not found")

    return air_conditioners


# Rota get ar condicionado por id
@app.get("/get-air-conditioner/{air_conditioner_id}")
async def get_room(air_conditioner_id: str, db: Session = Depends(get_db)):
    air_conditioner = retrieve_air_conditioner(air_conditioner_id, db)
    if not air_conditioner:
        return HTTPException(status_code=404, detail="Air Conditioner not found")

    return air_conditioner

# Rota deletar cômodo
@app.delete("/delete-air_conditioner/{air_conditioner_id}")
async def delete_room(air_conditioner_id: str, db: Session = Depends(get_db)):
    air_conditioner = remove_air_conditioner(air_conditioner_id, db)
    if not air_conditioner:
        return HTTPException(status_code=404, detail="Air Conditioner not deleted")

    return {"Message": f"Air Conditioner '{air_conditioner}' deleted successfully"}


# Rota atualizar cômodo
@app.put("/update-air_conditioner/{air_conditioner_id}")
async def update_room(air_conditioner_id: str, new_air_conditioner: UpdateAirConditioner, db: Session = Depends(get_db)):
    air_conditioner = change_air_conditioner(
        air_conditioner_id, new_air_conditioner, db)
    if not air_conditioner:
        return HTTPException(status_code=404, detail="Air Conditioner not updated")

    return {"Message": f"Air Conditioner '{air_conditioner}' updated successfully"}
