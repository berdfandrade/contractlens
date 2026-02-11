class RefreshTokenRepository:
    def __init__(self, db):
        self.collection = db.refresh_tokens

    async def save_token(self, user_id: str, token: str):
        await self.collection.insert_one(
            {
                "user_id": user_id,
                "token": token,
            }
        )

    async def get_token(self, token: str):
        return await self.collection.find_one({"token": token})

    async def delete_token(self, token: str):
        await self.collection.delete_one({"token": token})

    async def rotate_token(self, old_token: str, new_token: str):
        await self.collection.update_one(
            {"token": old_token}, {"$set": {"token": new_token}}
        )
