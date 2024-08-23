from aiopg import Connection
from bot.user.models import User
from bot.user_status import UserStatus


async def get_user(
    conn,
    tg_user_id: str | None = None,
    win_user_id: str | None = None,
) -> User | None:
    cur = await conn.cursor()

    conditions = []
    args = []

    if tg_user_id:
        conditions.append(f"tg_user_id = %s")
        args.append(tg_user_id)

    if win_user_id:
        conditions.append(f"win_user_id = %s")
        args.append(win_user_id)

    await cur.execute("SELECT * FROM users WHERE " + " ".join(conditions), args)
    user = await cur.fetchone()

    if user is None:
        return None

    return User(
        id=user[0],
        tg_user_id=user[1],
        win_user_id=user[2],
        status=user[3],
        chat_id=user[4],
    )


async def get_users(
    conn: Connection,
    status: UserStatus | None = None,
) -> list[User]:
    cur = await conn.cursor()

    conditions = []
    args = []

    if status:
        conditions.append(f"status = %s")
        args.append(status.value)

    await cur.execute("SELECT * FROM users WHERE " + " ".join(conditions), args)
    users = await cur.fetchall()

    return [
        User(
            id=user[0],
            tg_user_id=user[1],
            win_user_id=user[2],
            status=user[3],
            chat_id=user[4],
        )
        for user in users
    ]


async def create_user(conn: Connection, user: User):
    cur = await conn.cursor()
    await cur.execute(
        f"INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s)",
        (
            user.tg_user_id,
            user.win_user_id,
            user.status.value,
            user.chat_id,
        ),
    )
