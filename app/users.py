# ユーザー管理の簡易実装（本番ではDB推奨）
from typing import Dict

users: Dict[str, str] = {}  # user_id: role

def register_user(user_id: str, role: str):
    users[user_id] = role
    return {"user_id": user_id, "role": role}

def get_user(user_id: str):
    return users.get(user_id)
