from ..db import record
from ..src import _bot


async def get_channel(guild_id: int):
    channel_id = await record('SELECT log_ch FROM channels WHERE guild_id = %s', guild_id)
    if channel_id:
        channel = _bot.get_channel(channel_id)

        return channel
