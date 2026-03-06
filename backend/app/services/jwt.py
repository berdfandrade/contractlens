import uuid
from typing import Any, Mapping
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings
from app.services.errors.jwt import MustProvideSecretKeyError


class JwtService:
    SECRET_KEY = settings.jwt_secret_key
    ALGORITHM = settings.algorithm

    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def _create_token(cls, payload: Mapping[str, Any], expires_delta: timedelta) -> str:

        if not cls.SECRET_KEY:
            raise MustProvideSecretKeyError()

        now = datetime.now(timezone.utc)

        data = dict(payload)
        data.update(
            {
                "exp": now + expires_delta,
                "iat": now,
            }
        )

        return jwt.encode(data, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_access_token(cls, user_id: str) -> str:
        return cls._create_token(
            {"sub": user_id, "type": "access"},
            timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    @classmethod
    def create_refresh_token(cls, user_id: str) -> str:
        return cls._create_token(
            {
                "sub": user_id,
                "type": "refresh",
                "jti": str(uuid.uuid4()),
            },
            timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS),
        )

    @classmethod
    def decode_token(cls, token: str) -> Mapping[str, Any]:
        try:
            return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        except JWTError:
            raise
