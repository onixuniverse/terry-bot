from utils.configs import read_config


async def get_channel(bot, guild_id, channel_name: str):
    channel_id = read_config(str(guild_id), channel_name)

    if channel_id:
        channel = bot.get_channel(int(channel_id))

        return channel
