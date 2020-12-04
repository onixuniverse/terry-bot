import re

from bin.utils.channels import get_channel
from discord import Embed
from discord.ext.commands import Cog
from resources.data.regex import REGEX

from .. import db


class Abusing(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        """Antimat system."""
        if not message.author.bot:
            status = await db.record('SELECT abuse FROM configs WHERE guild_id'
                                     ' = %s', message.guild.id)

            if status == 'on':
                result = re.findall(REGEX, message.content)
                bad_words = []

                for match in result:
                    for word in match:
                        if word != '':
                            bad_words.append(word)

                if bad_words:
                    log_channel = await get_channel(message.guild.id)

                    embed = Embed(title=':mute: Антимат', color=0xa93226)
                    embed.set_thumbnail(url=message.author.avatar_url)

                    fields = [('Пользователь', message.author.mention, True),
                              ('Никнейм', message.author, True),
                              ('ID', message.author.id, True),
                              ('Контент сообщения', message.content, False),
                              ('Слова нецензурной лексики',
                               ', '.join(bad_words), False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Abusing(bot))
