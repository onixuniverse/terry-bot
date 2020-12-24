from .. import db
from ..src import bot


async def get_role(guild_id: int, role: str):
    """Функция получает ID роли из БД
    Доступные роли: `guest_role`"""
    guild = bot.get_guild(guild_id)

    role_id = await db.record(f'SELECT {role} FROM roles WHERE guild_id = %s',
                              guild_id)
    if role_id:
        role = guild.get_role(role_id)

        return role
