from app.services.errors.auth import InvalidRefreshToken


class TokenService:
    def __init__(self, jwt_service, refresh_repo):
        self.jwt_service = jwt_service
        self.refresh_repo = refresh_repo

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
