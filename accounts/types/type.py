from typing import TypedDict


class UserType(TypedDict):
    id: int
    name: str
    email: str
    avatar: str | None
    is_active: bool | None
    is_staff: bool | None
    is_superuser: bool | None