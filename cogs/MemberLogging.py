from typing import Union

from nextcord import Embed, Guild, Member, User
from nextcord.ext.commands import Cog

from utils.channels import get_channel
from utils.configs import read_config


async def create_event_embed(event_text: str, user: Union[Member, User], color: hex) -> Embed:
    embed = Embed(title=f'Событие: {event_text}', color=color)
    embed.set_thumbnail(url=user.avatar.url)

    fields = [('Пользователь', user.mention),
              ('Никнейм', user)]

    for name, value in fields:
        embed.add_field(name=name, value=value, inline=False)

    return embed


async def send_log_message(bot, user: Union[Member, User], guild: Guild, event_text: str, color: hex):
    status = bool(read_config(guild.id, "log_mode"))

    if status:
        channel = await get_channel(bot, guild.id, "log")

        await channel.send(embed=await create_event_embed(event_text, user, color))


class MemberLogging(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        """Логирование присоединение юзера к серверу"""
        await send_log_message(self.bot, member, member.guild, "Подключился к серверу", 0x21d92d)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Логирование выхода юзера с сервера"""
        await send_log_message(self.bot, member, member.guild, "Вышел с сервера", 0x1c88e6)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        """Логирование блокировок на сервере"""
        await send_log_message(self.bot, user, guild, "Пользователь забанен", 0xe6291c)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        """Логирование разблокировок на сервере"""
        await send_log_message(self.bot, user, guild, "Пользователь разбанен", 0x8e12cc)


def setup(bot):
    bot.add_cog(MemberLogging(bot))
