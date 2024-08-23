import aiopg
from bot.config_reader import config


def create_connection():
    return aiopg.connect(
        database=config.database,
        user=config.user,
        password=config.password_db,
        host=config.host.get_secret_value(),
    )
