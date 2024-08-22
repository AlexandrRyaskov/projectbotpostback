import asyncio
import aiopg
from fastapi import FastAPI
from bot.config_reader import config
from bot.user_status import UserStatus


app = FastAPI()


@app.get("/user/registered/{tg_user_id}/{win_user_id}")
async def read_item(tg_user_id: int, password: str, win_user_id: int):
    if password != config.postback_password.get_secret_value():
        return

    conn = await aiopg.connect(
        database=config.database,
        user=config.user,
        password=config.password_db,
        host=config.host.get_secret_value(),
    )
    cur = await conn.cursor()
    await cur.execute(
        f"UPDATE 1winreg WHERE tg_id = {tg_user_id} SET status = {UserStatus.REGISTERED}, win_user_id = {win_user_id}"
    )
    await conn.close()


@app.get("/user/made_deposit/{win_user_id}")
async def read_item(win_user_id: int, password: str):
    if password != config.postback_password.get_secret_value():
        return

    conn = await aiopg.connect(
        database=config.database,
        user=config.user,
        password=config.password_db,
        host=config.host.get_secret_value(),
    )
    cur = await conn.cursor()
    await cur.execute(
        f"UPDATE 1winreg WHERE win_user_id = {win_user_id} SET status = {UserStatus.MADE_DEPOSIT}"
    )
    await conn.close()


# http://abc.com/user/registered/{sub1}/{user_id}

#

if __name__ == "__main__":
    asyncio.run(read_item)
