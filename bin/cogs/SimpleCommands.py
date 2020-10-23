from discord import Embed, Member, Role
from discord.ext.commands import Cog
from discord.ext.commands import command, is_owner, group, cooldown
from discord.ext.commands import MemberNotFound
from discord.ext.commands import BucketType
from discord.ext.commands.core import bot_has_permissions, has_permissions
from discord.ext.commands.errors import CommandOnCooldown


from ..src import bot


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command(name='addrole',
           aliases=['addroles', 'roleadd', 'rolesadd'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def give_role(self, ctx, member: Member, *roles: Role):
        if member:
            await member.add_roles(*roles, reason=f'Выдана: {ctx.message.author}')
    
    @group(name='hug')
    @cooldown(1, 5, BucketType.user)
    async def hugs(self, ctx, member: Member=None):
        if member and ctx.message.author is not member:
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
