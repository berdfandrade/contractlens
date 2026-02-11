from app.services.jwt import JwtService
from app.services.user import UserService
from app.services.hash import HashService
from pydantic import EmailStr
from app.services.errors.auth import EmailNotRegistered


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        hash_service: HashService,
        jwt_service: JwtService,
    ):
        self.user_service = user_service
        self.hash_service = hash_service
        self.jwt_service = jwt_service

    async def authenticate_user(self, email: EmailStr, password: str):
        user = await self.user_service.get_user_with_password(email)

        if not user:
            raise EmailNotRegistered()

        if not self.hash_service.verify_password(
            password,
            user["password"],
        ):
            return None

        return self.user_service._serialize_user(user)

    def login_user(self, user):
        return self.jwt_service.create_access_token({"sub": user["id"]})
