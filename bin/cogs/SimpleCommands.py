from typing import Optional

from discord import Embed, Member, Role
from discord.ext.commands import (BucketType, Cog, Greedy, bot_has_permissions,
                                  command, cooldown, group, has_permissions,
                                  is_owner)

from ..src import bot


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        
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

    @command(name='addrole',
           aliases=['addroles', 'roleadd', 'rolesadd'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def give_role(self, ctx, member: Member, *roles: Role):
        await member.add_roles(*roles, reason=f'Выдана: {ctx.message.author}')
    
    @group(name='hug')
    @cooldown(1, 5, BucketType.user)
    async def hugs(self, ctx, member: Member):
        if ctx.message.author is not member:
            await ctx.send(f'**:hugging: | {ctx.message.author.mention} обнял(а) {member.mention}**')

    @command(name='guilds')
    @is_owner()
    async def get_guilds(self, ctx):
        guilds_list = bot.guilds
        guilds = ''

        emb = Embed(color=0xf454f3,
                    title='Список серверов')
        
        for guild in guilds_list:
            guilds += guild.name
                
        emb.description = guilds
        
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
