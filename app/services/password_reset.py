import secrets
import hashlib
from datetime import datetime, timedelta
from bson import ObjectId


class PasswordResetService:

    def __init__(self, db, hash_service, mail_service):
        self.db = db
        self.hash_service = hash_service
        self.mail_service = mail_service

    def _generate_token(self) -> str:
        return secrets.token_urlsafe(48)

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def request_password_reset(self, email: str):

        user = await self.db.users.find_one({"email": email})
        if not user:
            return

        raw_token = self._generate_token()
        token_hash = self._hash_token(raw_token)

        expires_at = datetime.now() + timedelta(minutes=30)

        # Remove tokens antigos do usuário
        await self.db.password_reset_tokens.delete_many({"user_id": str(user["_id"])})

        await self.db.password_reset_tokens.insert_one(
            {
                "user_id": str(user["_id"]),
                "token_hash": token_hash,
                "created_at": datetime.now(),
                "expires_at": expires_at,
            }
        )

        reset_link = f"http://localhost:8000/reset-password?token={raw_token}"

        await self.mail_service.send_email(
            to=user["email"],
            subject="Redefinição de senha - Contract Lens",
            body=f"Clique no link para redefinir sua senha:\n{reset_link}",
            html=f"""
            <h2>Redefinição de senha</h2>
            <p>Clique no botão abaixo:</p>
            <a href="{reset_link}" 
               style="padding:10px 15px;background:#111;color:white;text-decoration:none;">
               Redefinir senha
            </a>
            """,
        )

    async def reset_password(self, token: str, new_password: str):

        token_hash = self._hash_token(token)

        reset_doc = await self.db.password_reset_tokens.find_one(
            {"token_hash": token_hash}
        )

        if not reset_doc:
            raise ValueError("Invalid or expired token")

        if reset_doc["expires_at"] < datetime.now():
            raise ValueError("Token expired")

        user_id = reset_doc["user_id"]

        hashed_password = self.hash_service.hash_password(new_password)

        await self.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"password": hashed_password}}
        )

        await self.db.password_reset_tokens.delete_many({"user_id": user_id})
