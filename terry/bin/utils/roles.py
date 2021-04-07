from .. import db
from ..src import _bot


async def get_role(guild_id: int, role: str):
    """Получает ID роли из БД"""
    guild = _bot.get_guild(guild_id)

    role_id = await db.record(f'SELECT {role} FROM roles WHERE guild_id = %s', guild_id)
    if role_id:
        role = guild.get_role(role_id)

        return role
