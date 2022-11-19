import re

from nextcord import Embed
from nextcord.ext.commands import Cog

from utils.channels import get_channel
from utils.configs import read_config
from utils.regex import REGEX


class AntimatHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        """Система антимата"""
        if not message.author.bot:
            try:
                status = bool(read_config(message.guild.id, "abuse_mode"))
            except KeyError:
                status = None

            if status:
                result = re.findall(REGEX, message.content)
                bad_words = []

                for match in result:
                    for word in match:
                        if word != '':
                            bad_words.append(word)

                if bad_words:
                    log_channel = await get_channel(self.bot, message.guild.id, "log_channel_id")
                    print(log_channel)

                    if log_channel:
                        embed = Embed(title=':mute: Антимат', color=0xa93226)
                        embed.set_thumbnail(url=message.author.avatar.url)

                        fields = [('Пользователь', message.author.mention, True),
                                  ('Никнейм', message.author, True),
                                  ('ID', message.author.id, True),
                                  ('Контент сообщения', message.content, False),
                                  ('Слова нецензурной лексики', ', '.join(bad_words), False)]

                        for name, value, inline in fields:
                            embed.add_field(name=name, value=value, inline=inline)

                        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(AntimatHandler(bot))
