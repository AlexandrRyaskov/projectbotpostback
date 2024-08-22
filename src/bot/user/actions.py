from bot.user.models import User


async def get_user(
    conn,
    tg_user_id: int | None = None,
    win_user_id: int | None = None,
) -> User | None:
    cur = await conn.cursor()

    conditions = []

    if tg_user_id:
        conditions.append(f"tg_id = {tg_user_id}")
    if win_user_id:
        conditions.append(f"win_user_id = {win_user_id}")

    await cur.execute("SELECT * FROM users WHERE " + " ".join(conditions))
    user = await cur.fetchone()

    if user is None:
        return None

    return User(tg_id=user[0], status=user[1])


async def create_user(conn, user: User):
    cur = await conn.cursor()
    await cur.execute(f"INSERT INTO users VALUES ({user.tg_id}, '{user.status.value}')")
