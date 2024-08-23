import asyncio
from fastapi import FastAPI
from bot.config_reader import config
from bot.database import create_connection
from bot.user_status import UserStatus


app = FastAPI()


@app.get("/user/registered/{win_user_id}")
async def read_item(tg_user_id: str, password: str, win_user_id: str):
    if password != config.postback_password.get_secret_value():
        return

    async with create_connection() as conn:
        cur = await conn.cursor()
        await cur.execute(
            "UPDATE users SET status = %s, win_user_id = %s WHERE tg_user_id = %s",
            (
                UserStatus.REGISTERED.value,
                win_user_id,
                tg_user_id,
            ),
        )


@app.get("/user/made_deposit/{win_user_id}")
async def read_item(win_user_id: str, password: str):
    if password != config.postback_password.get_secret_value():
        return

    async with create_connection() as conn:
        cur = await conn.cursor()
        await cur.execute(
            "UPDATE users SET status = %s WHERE win_user_id = %s",
            (
                UserStatus.MADE_DEPOSIT.value,
                win_user_id,
            ),
        )


# http://abc.com/user/registered/{user_id}/?tg_user_id={sub1}
# http://abc.com/user/made_deposit/{user_id}

#

if __name__ == "__main__":
    asyncio.run(read_item)
