from typing import Optional

from .core import ApiRequest
from .types import Token, UserResponse, Admin


class ApiManager(ApiRequest):
    async def get_token(self, username: str, password: str) -> Optional[Token]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return await self.post(
            endpoint="/api/admin/token",
            data=data,
            response_model=Token,
        )

    async def get_users(
        self,
        access: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        owner_username: Optional[str] = None,
    ) -> Optional[list[UserResponse]]:
        users = await self.get(
            endpoint="/api/users",
            params={
                "offset": offset,
                "limit": limit,
                "admin": owner_username,
            },
            access=access,
        )
        if not users:
            return False
        return [UserResponse(**user) for user in users["users"]]

    async def get_user(self, username: str, access: str) -> Optional[UserResponse]:
        return await self.get(
            endpoint=f"/api/user/{username}",
            access=access,
            response_model=UserResponse,
        )

    async def create_admin(
        self, username: str, password: str, access: str
    ) -> Optional[Admin]:
        return await self.post(
            endpoint="/api/admin",
            access=access,
            data={"username": username, "password": password, "is_sudo": False},
            response_model=Admin,
        )

    async def create_user(self, data: dict, access: str) -> Optional[UserResponse]:
        return await self.post(
            endpoint="/api/user",
            access=access,
            data=data,
            response_model=UserResponse,
        )

    async def modify_user(self, data: dict, username: str,access: str) -> Optional[UserResponse]:
        return await self.put(
            endpoint=f"/api/user/{username}",
            access=access,
            data=data,
            response_model=UserResponse,
        )