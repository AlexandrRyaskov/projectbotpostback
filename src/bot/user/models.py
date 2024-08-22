from pydantic import BaseModel

from bot.user_status import UserStatus


EMPTY_ID = -1


class User(BaseModel):
    id: int = EMPTY_ID
    chat_id: str
    tg_user_id: str
    win_user_id: str | None = None
    status: UserStatus
