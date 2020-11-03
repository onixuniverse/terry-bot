import re

from bin.utils import get_channel
from resources.data.regex import REGEX
from discord import Embed
from discord.ext.commands import Cog

from .. import db


class Abusing(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        """Antimat system."""
        if not message.author.bot:
            status = await db.record('SELECT abuse FROM configs WHERE guild_id = %s', message.guild.id)

            if status == 'on':
                result = re.findall(REGEX, message.content)
                bad_words = []

                for match in result:
                    for word in match:
                        if word != '':
                            bad_words.append(word)

                if bad_words:
                    log_channel = await get_channel(message.guild.id)

                    emb = Embed(color=0xa93226)
                    emb.title = ':mute: Антимат'
                    emb.add_field(name='Пользователь', value=message.author.mention, inline=True)
                    emb.add_field(name='Никнейм', value=message.author, inline=True)
                    emb.add_field(name='ID', value=message.author.id, inline=True)
                    emb.add_field(name='Контент сообщения', value=message.content, inline=False)
                    emb.add_field(name='Слова нецензурной лексики', value=str(', '.join(bad_words)), inline=False)
                    emb.set_thumbnail(url=message.author.avatar_url)
                    await log_channel.send(embed=emb)


def setup(bot):
    bot.add_cog(Abusing(bot))
