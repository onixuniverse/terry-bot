from ..src import bot
from .. import db


async def get_channel(guild_id: int):
    channel_id = await db.record('SELECT log_ch FROM channels WHERE guild_id = %s', guild_id)
    if channel_id:
        channel = bot.get_channel(channel_id)
        
        return channel


async def get_role(guild_id: int):
    guild = bot.get_guild(guild_id)
    
    role_id = await db.record('SELECT guest_role FROM roles WHERE guild_id = %s', guild_id)
    if role_id:
        role = guild.get_role(role_id)
        
        return role
