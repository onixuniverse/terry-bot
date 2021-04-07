from discord import Embed
from discord.errors import HTTPException
from discord.ext.commands import Cog

from .. import db
from ..utils.channels import get_channel


class MessageLogging(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_message_delete(self, payload):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', payload.guild_id)

        if status == 'on':
            message = payload.cached_message

            if message and not message.author.bot:
                log_channel = await get_channel(payload.guild_id)
                msg_channel = self.bot.get_channel(payload.channel_id)

                embed = Embed(title=':wastebasket: Сообщение было удалено', color=0xFF5733)
                embed.add_field(name='Автор', value=message.author.mention, inline=True)
                embed.add_field(name='Канал', value=msg_channel.mention, inline=True)

                if message.content:
                    embed.add_field(name='Контент', value=message.content, inline=True)

                if message.attachments:
                    image_url = message.attachments[0].proxy_url
                    try:
                        embed.set_image(url=image_url)
                    except HTTPException:
                        await log_channel.send('Ошибка изображения: ', HTTPException)

                await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', payload.guild_id)

        if status == 'on':
            messages = payload.cached_messages

            if messages:
                log_channel = await get_channel(payload.guild_id)
                msg_channel = self.bot.get_channel(payload.channel_id)

                embed = Embed(title=':wastebasket: Группа сообщений была удалена', color=0xFF5733)
                embed.add_field(name='Канал', value=msg_channel.mention, inline=True)
                embed.add_field(name='Количество', value=len(messages), inline=True)

                await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogging(bot))
