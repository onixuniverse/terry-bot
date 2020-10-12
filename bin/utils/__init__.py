import discord

from bin.bot import bot
from ..db import db


async def get_channel(guild_id: int):
    channel_id = db.execute('SELECT log_ch FROM channels WHERE guild_id = %s', guild_id)
    if channel_id:
        channel = bot.get_channel(channel_id)
        
        return channel
    else:
        pass
