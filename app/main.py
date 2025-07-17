from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from typing import List
from .users import register_user, get_user
from .chat_rooms import create_room, join_room, get_room_users

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Chat API is running. See /docs for API documentation."}

@app.post("/register")
async def register(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    role = data.get("role")
    return register_user(user_id, role)

@app.get("/user/{user_id}")
async def get_user_info(user_id: str):
    role = get_user(user_id)
    return {"user_id": user_id, "role": role}

@app.post("/room")
async def create_chat_room(request: Request):
    data = await request.json()
    room_id = data.get("room_id")
    return create_room(room_id)

@app.post("/room/join")
async def join_chat_room(request: Request):
    data = await request.json()
    room_id = data.get("room_id")
    user_id = data.get("user_id")
    return join_room(room_id, user_id)

@app.get("/room/{room_id}/users")
async def get_room_user_list(room_id: str):
    users = get_room_users(room_id)
    return {"room_id": room_id, "users": users}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Room {room_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
