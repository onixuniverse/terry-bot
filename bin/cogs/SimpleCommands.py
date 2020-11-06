from discord import Member
from discord.ext.commands import BucketType, Cog, cooldown, group


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @group(name='hug')
    @cooldown(1, 5, BucketType.user)
    async def hugs(self, ctx, member: Member):
        if ctx.message.author is not member:
            await ctx.send(f'**:hugging: | {ctx.message.author.mention} обнял(а) {member.mention}**')


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
