from jose import jwt, ExpiredSignatureError, JWTError
from app.services.errors.auth import InvalidRefreshToken
from app.core.config import settings
from datetime import datetime, timedelta


class TokenService:
    def __init__(
        self, jwt_service, refresh_repo, secret_key=settings.reset_token_secret
    ):
        self.jwt_service = jwt_service
        self.refresh_repo = refresh_repo
        self.secret_key = settings.reset_token_secret

    async def create_session(self, user_id: str):
        access_token = self.jwt_service.create_access_token({"sub": user_id})

        refresh_token = self.jwt_service.create_refresh_token({"sub": user_id})

        await self.refresh_repo.save_token(
            user_id=user_id,
            token=refresh_token,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_session(self, refresh_token: str):
        payload = self.jwt_service.decode_token(refresh_token)

        stored = await self.refresh_repo.get_token(refresh_token)
        if not stored:
            raise InvalidRefreshToken()

        user_id = payload["sub"]

        new_access = self.jwt_service.create_access_token({"sub": user_id})
        new_refresh = self.jwt_service.create_refresh_token({"sub": user_id})

        await self.refresh_repo.rotate_token(
            old_token=refresh_token,
            new_token=new_refresh,
        )

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }

    async def revoke_session(self, refresh_token: str):
        await self.refresh_repo.delete_token(refresh_token)

    def create_reset_token(self, user_id: str, expires_minutes: int = 30) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_reset_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload.get("sub")
        except (ExpiredSignatureError, JWTError):
            return None
