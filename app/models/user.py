from datetime import datetime
from pydantic import BaseModel
from app.api.types import UserStatus, UserDataUsageResetStrategy


class UserCreate(BaseModel):
    username: str
    data_limit: int
    data_limit_reset_strategy: UserDataUsageResetStrategy
    inbounds: dict = {}
    proxies: dict
    status: UserStatus
    expire: int | None = None
    note: str | None = ""
    on_hold_expire_duration: int | None = None
    created_at: datetime | None = None
    sub_revoked_at: datetime | None = None
