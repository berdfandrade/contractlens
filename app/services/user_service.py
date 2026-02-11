from unittest import result

from bson import ObjectId
from app.core.database import get_database
from app.models.user import UserCreate

class UserService:
    @staticmethod
    async def create_user(user: UserCreate):
        db = get_database()
        user_dict = user.model_dump()
        result = await db.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return user_dict

    @staticmethod
    async def get_user(user_id: str):
        db = get_database()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        user["id"] = str(user["_id"])
        del user["_id"]

        return user