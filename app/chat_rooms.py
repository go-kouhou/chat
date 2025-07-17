# チャットルーム管理の簡易実装
from typing import Dict, List

chat_rooms: Dict[str, List[str]] = {}  # room_id: [user_id]

def create_room(room_id: str):
    if room_id not in chat_rooms:
        chat_rooms[room_id] = []
    return {"room_id": room_id}

def join_room(room_id: str, user_id: str):
    if room_id in chat_rooms:
        if user_id not in chat_rooms[room_id]:
            chat_rooms[room_id].append(user_id)
    return {"room_id": room_id, "users": chat_rooms[room_id]}

def get_room_users(room_id: str):
    return chat_rooms.get(room_id, [])
