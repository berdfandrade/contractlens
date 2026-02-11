import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


class JwtService:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @classmethod
    def create_access_token(cls, data: dict):
        if not cls.SECRET_KEY:
            raise ValueError("MUST PROVIDE SECRET_KEY")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_access_token(cls, token: str) -> dict | None:
        if not cls.SECRET_KEY:
            raise ValueError("MUST PROVIDE SECRET_KEY")
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            return None
