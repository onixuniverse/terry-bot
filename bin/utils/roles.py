import db
from src import bot


async def get_role(guild_id: int, role: str):
    guild = bot.get_guild(guild_id)

    role_id = await db.record(f'SELECT {role} FROM roles WHERE guild_id = %s',
                              guild_id)
    if role_id:
        role = guild.get_role(role_id)

        return role


async def get_guest_role(guild_id: int):
    guest_role = await get_role(guild_id, 'guest_role')

    return guest_role


async def get_curator_role(guild_id: int):
    curator_role = await get_role(guild_id, 'curator_role')

    return curator_role
