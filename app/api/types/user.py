from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel
from .admin import Admin


class UserDataUsageResetStrategy(str, Enum):
    no_reset = "no_reset"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LIMITED = "limited"
    EXPIRED = "expired"
    ONHOLD = "on_hold"


class UserResponse(BaseModel):
    username: Optional[str] = None
    proxies: Optional[Dict[str, dict]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: UserDataUsageResetStrategy = (
        UserDataUsageResetStrategy.no_reset
    )
    inbounds: Optional[Dict[str, List[str]]] = None
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[datetime] = None
    sub_updated_at: Optional[datetime] = None
    status: UserStatus = UserStatus.ACTIVE
    used_traffic: Optional[int] = None
    lifetime_used_traffic: Optional[int] = None
    links: Optional[List[str]] = []
    subscription_url: Optional[str] = None
    excluded_inbounds: Optional[Dict[str, List[str]]] = None
    admin: Optional[Admin] = None
    created_at: Optional[datetime] = None
