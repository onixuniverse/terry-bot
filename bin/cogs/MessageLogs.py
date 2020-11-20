from bin.utils.channels import get_channel
from discord import Embed
from discord.ext.commands import Cog

from .. import db

class MessageLogs(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_message_delete(self, payload):
        status = await db.record('SELECT logging FROM configs WHERE  guild_id = %s', payload.guild_id)
        
        if status == 'on':
            message = payload.cached_message

            if message:
                log_channel = await get_channel(payload.guild_id)
                msg_channel = self.bot.get_channel(payload.channel_id)
                
                embed = Embed(title='Сообщение было удалено',
                              color=0xFF5733)
                fields = [('ID', payload.message_id, True),
                        ('Автор', message.author, True),
                        ('Канал', msg_channel.name, True),
                        ('Контент', message.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogs(bot))
