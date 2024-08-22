from pydantic import BaseModel

from bot.user_status import UserStatus


class User(BaseModel):
    tg_id: int
    win_id: int
    status: UserStatus
