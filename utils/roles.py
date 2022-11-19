from utils.configs import read_config


async def get_role(bot, guild_id, role_name: str):
    """Получает ID роли из конфиг-файла"""
    guild = bot.get_guild(guild_id)

    role_id = read_config(str(guild_id), role_name)

    if role_id:
        role = guild.get_role(int(role_id))

        return role
