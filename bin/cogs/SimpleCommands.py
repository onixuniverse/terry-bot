from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command, is_owner, group, cooldown
from discord.ext.commands import MemberNotFound
from discord.ext.commands import BucketType
from discord.ext.commands.errors import CommandOnCooldown


from ..src import bot


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @group(name='hug')
    @cooldown(1, 5, BucketType.user)
    async def hugs(self, ctx, member: Member=None):
        if member and ctx.message.author is not member:
            await ctx.send(f'**:hugging: | {ctx.message.author.mention} обнял(а) {member.mention}**')
    
    @hugs.error
    async def hugs_error(self, ctx, exc):
        if isinstance(exc, MemberNotFound):
            await ctx.send(f'**[E]** | {ctx.message.author.mention}, обнимать можно только настоящих пользователей.')
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(f'**[E]** | {ctx.message.author.mention}, комманда под задержкой. Осталось: {round(exc.retry_after)}сек.', delete_after=exc.retry_after)
    
    @command(name='guilds')
    @is_owner()
    async def get_guilds(self, ctx):
        guilds_list = bot.guilds

        emb = Embed(color=0xf454f3,
                    title='Список серверов')
        for name, value, inline in guilds_list:
            emb.add_field(name=name, value=value, inline=inline)
        
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
