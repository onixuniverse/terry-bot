from typing import Optional

from bin.src import bot
from bin.utils import get_channel
from discord import Embed, Member, Role
from discord.ext.commands import (Cog, Greedy, bot_has_permissions, command,
                                  has_permissions, is_owner)


class ModerCommand(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='kick')
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    async def kick_member(self, ctx, targets: Greedy[Member], *, reason: Optional[str]='Нет видимой причины.'):
        channel = await get_channel(ctx.guild.id)
        
        for user in targets:
            await user.kick(reason=reason)
            
            emb = Embed(color=0x19BCB0)
            emb.title = '**Пользователь кикнут командой**'
            fields = [('Пользователь', user.mention, True),
                      ('Никнейм', user, True),
                      ('Причина', reason, False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
            
            await channel.send(embed=emb)
    
    @command(name='ban')
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban_member(self, ctx, targets: Greedy[Member], *, reason: Optional[str]='Нет видимой причины.'):
        
        for user in targets:
            await user.ban(reason=reason)
            
    @command(name='clear', aliases=['purge'])
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int]=1):
        def _check(message):
            return not len(targets) or message.author in targets
        
        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, check=_check)
                await ctx.send(f'{len(deleted):,} сообщений было удалено.', delete_after=5)
        else:
            await ctx.send('Неверное количество удаляемых сообщений.')

    
    @command(name='guilds')
    @is_owner()
    async def get_guilds(self, ctx):
        guilds_list = bot.guilds
        guilds = []

        emb = Embed(color=0xf454f3,
                    title='Список серверов')
        
        for guild in guilds_list:
            guilds.append(guild)
        
        await ctx.send(embed=emb)
        
        
    @command(name='addrole',
           aliases=['addroles', 'roleadd', 'rolesadd'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def give_role(self, ctx, member: Member, *roles: Role):
        await member.add_roles(*roles, reason=f'Выдана: {ctx.message.author}')

def setup(bot):
    bot.add_cog(ModerCommand(bot))
