from bson import ObjectId
from app.core.database import get_database
from app.services.hash import HashService
from app.models.user import UserCreate


class UserService:
    def __init__(self, db, hash_service: HashService):
        self.db = db
        self.hash_service = hash_service

    async def create_user(self, user: UserCreate):

        existing_user = await self.db.users.find_one({"email": user.email})

        if existing_user:
            raise ValueError("User already exists")

        user_dict = user.model_dump()
        user_dict["password"] = self.hash_service.hash_password(user.password)

        result = await self.db.users.insert_one(user_dict)
        created_user = await self.db.users.find_one({"_id": result.inserted_id})
        return self._serialize_user(created_user)

    async def get_user(self, user_id: str):

        user = await self.db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            return None

        return self._serialize_user(user)

    def _serialize_user(self, user: dict):
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        user.pop("password", None)
        return user
