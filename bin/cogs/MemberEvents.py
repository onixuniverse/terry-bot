from discord import Embed
from discord.ext.commands import Cog

from ..utils import get_channel, get_role
from .. import db


class MemberEvents(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', member.guild.id)
        guest_status = await db.record('SELECT guest FROM configs WHERE guild_id = %s', member.guild.id)
        
        if status:
            channel = await get_channel(member.guild.id)
            
            emb = Embed(color=0x21d92d,
                        title='Пользователь присоеденился к серверу')
            emb.add_field(name='Пользователь', value=member.mention, inline=False)
            emb.add_field(name='Никнейм', value=member, inline=False)
            emb.add_field(name='ID', value=member.id, inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=emb)
        
        if guest_status:
            role = await get_role(member.guild.id)
            if role:
                reason = 'Роль выдана системой "Гости"'
                
                await member.add_roles(role, reason=reason)

    @Cog.listener()
    async def on_member_remove(self, member):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', member.guild.id)
        
        if status:
            channel = await get_channel(member.guild.id)
            
            emb = Embed(color=0x1c88e6,
                        title='Пользователь вышел с сервера')
            emb.add_field(name='Пользователь', value=member.mention, inline=False)
            emb.add_field(name='Никнейм', value=member, inline=False)
            emb.add_field(name='ID', value=member.id, inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=emb)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', guild.id)
        
        if status:
            channel = await get_channel(guild.id)
            
            emb = Embed(color=0xe6291c,
                        title='Пользователь забанен')
            emb.add_field(name='Пользователь', value=user.mention, inline=False)
            emb.add_field(name='Никнейм', value=user, inline=False)
            emb.add_field(name='ID', value=user.id, inline=False)
            emb.set_thumbnail(url=user.avatar_url)
            await channel.send(embed=emb)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', guild.id)
        
        if status:
            channel = await get_channel(guild.id)
            
            emb = Embed(color=0x8e12cc,
                        title='Пользователь разбанен')
            emb.add_field(name='Пользователь', value=user.mention, inline=False)
            emb.add_field(name='Никнейм', value=user, inline=False)
            emb.add_field(name='ID', value=user.id, inline=False)
            emb.set_thumbnail(url=user.avatar_url)
            await channel.send(embed=emb)


def setup(bot):
    bot.add_cog(MemberEvents(bot))
