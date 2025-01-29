from app.api.types import UserStatus, UserResponse
from app.models.user import UserCreate


def get_user_data_limit(user: UserResponse) -> int | None:
    if user.status in [UserStatus.LIMITED]:
        return 1024
    if not user.data_limit:
        return None
    if not user.used_traffic and user.data_limit:
        return user.data_limit
    if user.used_traffic and user.data_limit:
        return user.data_limit - user.used_traffic


def create_user_data(
    user: dict,
) -> dict:
    user: UserResponse = UserResponse(**user)
    datalimit = get_user_data_limit(user=user)
    status = (
        UserStatus.ONHOLD if user.status == UserStatus.ONHOLD else UserStatus.ACTIVE
    )
    is_onhold = UserStatus.ONHOLD == user.status
    data = UserCreate(
        username=user.username,
        data_limit=datalimit,
        data_limit_reset_strategy=user.data_limit_reset_strategy,
        inbounds={},
        proxies=user.proxies,
        status=status,
        expire=None if is_onhold else user.expire,
        note=user.note,
        on_hold_expire_duration=user.on_hold_expire_duration if is_onhold else None,
        created_at=user.created_at,
        sub_revoket_at=user.sub_revoked_at,
    ).dict()
    return data
