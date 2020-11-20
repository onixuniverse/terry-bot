from bin.utils.channels import get_channel
from bin.utils.roles import get_guest_role
from discord import Embed
from discord.ext.commands import Cog

from .. import db


class MemberLog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        """Logging system. Called when the user logs in to the guild."""
        status = await db.record('SELECT logging FROM configs WHERE  guild_id = %s', member.guild.id)
        guest_status = await db.record('SELECT guest FROM configs WHERE  guild_id = %s', member.guild.id)

        if status == 'on':
            channel = await get_channel(member.guild.id)

            embed = Embed(title='Подключился к серверу', color=0x21d92d)
            embed.set_thumbnail(url=member.avatar_url)

            fields = [('Пользователь', member.mention),
                      ('Никнейм', member),
                      ('ID', member.id)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)

        if guest_status:
            role = await get_guest_role(member.guild.id)
            if role:
                reason = 'Роль выдана системой "Гости"'

                await member.add_roles(role, reason=reason)

    @Cog.listener()
    async def on_member_remove(self, member):
        """Logging system. Called when the user leaves the guild."""
        status = await db.record('SELECT logging FROM configs WHERE guild_id'
                                 ' = %s', member.guild.id)

        if status == 'on':
            channel = await get_channel(member.guild.id)

            embed = Embed(title='Вышел с сервера', color=0x1c88e6)
            embed.set_thumbnail(url=member.avatar_url)

            fields = [('Пользователь', member.mention),
                      ('Никнейм', member),
                      ('ID', member.id)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        """Logging system. Called when the user is banned from the guild."""
        status = await db.record('SELECT logging FROM configs WHERE guild_id'
                                 ' = %s', guild.id)

        if status == 'on':
            channel = await get_channel(guild.id)

            embed = Embed(title='Пользователь забанен', color=0xe6291c)
            embed.set_thumbnail(url=user.avatar_url)

            fields = [('Пользователь', user.mention),
                      ('Никнейм', user),
                      ('ID', user.id)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        """Logging system. Called when the user is being unban on the guild."""
        status = await db.record('SELECT logging FROM configs WHERE guild_id'
                                 ' = %s', guild.id)

        if status == 'on':
            channel = await get_channel(guild.id)

            embed = Embed(title='Пользователь разбанен', color=0x8e12cc)
            fields = [('Пользователь', user.mention),
                      ('Никнейм', user),
                      ('ID', user.id)]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberLog(bot))
