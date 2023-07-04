from fastapi import FastAPI, HTTPException, WebSocket, Depends, WebSocketDisconnect
from schemas import Room, UpdateRoom, UpdateAirConditioner
from database import SessionLocal, database, engine
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from crud import (
    retrieve_all_rooms,
    retrieve_room,
    create_room,
    remove_room,
    change_room,
    retrieve_all_air_conditioners,
    retrieve_air_conditioner,
    remove_air_conditioner,
    change_air_conditioner
)

import models
import asyncio
import json


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)
notification_event = asyncio.Event()
app = FastAPI(
    title="Control Air",
    description="API para controle de ar condicionado",
    version="0.0.1",
    dependencies=[Depends(get_db)]
)


@app.on_event("startup")
async def startup():
    await database.connect()
    app.active_connections = set()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
       

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    app.active_connections.add(websocket)
    
    try:
        while True:
            await notification_event.wait()
            notification_event.clear()
            
            data = retrieve_all_rooms(db)
            for websocket in app.active_connections:
                await websocket.send_text(json.dumps({"message": data}))
            
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        app.active_connections.remove(websocket)

    
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
    
    if new_room.temperature or new_room.humidity:
        notification_event.set()
        
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
    air_conditioner = change_air_conditioner(air_conditioner_id, new_air_conditioner, db)
    if not air_conditioner:
        return HTTPException(status_code=404, detail="Air Conditioner not updated")

    return {"Message": f"Air Conditioner '{air_conditioner}' updated successfully"}
