from discord import Embed
from discord.ext.commands import Cog, command

from ..utils import get_channel


class Logging(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_member_join(self, member):
        channel = get_channel(member.guild.id)
        
        emb = Embed(color=0x25db44,
                    title='Логирование')
        emb.add_field(name='Присоединился к серверу', value=member.mention)
        await channel.send(embed=emb)
    
    @Cog.listener()
    async def on_member_remove(self, member):
        channel = get_channel(member.guild.id)
        
        emb = Embed(color=0x25db44,
                    title='Логирование')
        emb.add_field(name='Вышел с сервера', value=member.mention)
        await channel.send(embed=emb)
    
    @Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = get_channel(guild.id)
        
        emb = Embed(color=0x25db44,
                    title='Логирование')
        emb.add_field(name='Забанен', value=user.mention)
        await channel.send(embed=emb)
    
    @Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = get_channel(guild.id)
        
        emb = Embed(color=0x25db44,
                    title='Логирование')
        emb.add_field(name='Разбанен', value=user.mention)
        await channel.send(embed=emb)


def setup(bot):
    bot.add_cog(Logging(bot))
