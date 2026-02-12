import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


class JwtService:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def _create_token(cls, data: dict, expires_delta: timedelta):
        if not cls.SECRET_KEY:
            raise ValueError("MUST PROVIDE SECRET_KEY")

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_access_token(cls, data: dict):
        return cls._create_token(
            data,
            timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    @classmethod
    def create_refresh_token(cls, data: dict):
        return cls._create_token(
            data,
            timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS),
        )

    @classmethod
    def decode_token(cls, token: str) -> dict:
        if not cls.SECRET_KEY:
            raise ValueError("MUST PROVIDE SECRET_KEY")

        secret: str = cls.SECRET_KEY
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError as e:
            raise e
