from discord import Embed
from discord.errors import HTTPException
from discord.ext.commands import Cog

from .. import db
from ..utils.channels import get_channel


class MessageLogs(Cog):
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

                embed = Embed(title='Сообщение было удалено', color=0xFF5733)

                fields = [('Автор', message.author.mention, True),
                          ('Канал', msg_channel.mention, True)]

                if message.embeds:
                    fields.append(('Количество встроенных врезок', len(message.embeds), True))
                else:
                    if message.attachments:
                        if message.content:
                            fields.append(('Контент', message.content, False))

                        image_url = message.attachments[0].proxy_url
                        try:
                            embed.set_image(url=image_url)
                        except HTTPException:
                            fields.append(('Изображение', 'Изображение не найдено в кэше', True))
                    else:
                        fields.append(('Контент', message.content, False))

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', payload.guild_id)

        if status == 'on':
            messages = payload.cached_messages

            if messages:
                log_channel = await get_channel(payload.guild_id)
                msg_channel = self.bot.get_channel(payload.channel_id)

                embed = Embed(title='Группа сообщений была удалена', color=0xFF5733)

                fields = [('Канал', msg_channel.mention, True),
                          ('Количество сообщений', len(payload.cached_messages), True)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogs(bot))
