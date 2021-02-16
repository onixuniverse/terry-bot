from discord import Embed
from discord.ext.commands import Cog

from .. import db
from ..utils import get_channel


class MemberLogging(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        """Логирование присоединения к серверу"""
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', member.guild.id)

        if status == 'on':
            channel = await get_channel(member.guild.id)

            embed = Embed(title='Подключился к серверу', color=0x21d92d)
            embed.set_thumbnail(url=member.avatar_url)

            fields = [('Пользователь', member.mention),
                      ('Никнейм', member)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Логирование выходов с сервера"""
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', member.guild.id)

        if status == 'on':
            channel = await get_channel(member.guild.id)

            embed = Embed(title='Вышел с сервера', color=0x1c88e6)
            embed.set_thumbnail(url=member.avatar_url)

            fields = [('Пользователь', member.mention),
                      ('Никнейм', member)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        """Логирование банов на сервере"""
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', guild.id)

        if status == 'on':
            channel = await get_channel(guild.id)

            embed = Embed(title='Пользователь забанен', color=0xe6291c)
            embed.set_thumbnail(url=user.avatar_url)

            fields = [('Пользователь', user.mention),
                      ('Никнейм', user)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        """Логирование разбанов на сервере"""
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', guild.id)

        if status == 'on':
            channel = await get_channel(guild.id)

            embed = Embed(title='Пользователь разбанен', color=0x8e12cc)
            fields = [('Пользователь', user.mention),
                      ('Никнейм', user)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberLogging(bot))
