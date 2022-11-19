from nextcord.ext.commands import Cog, command


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(hidden=True)
    async def status(self, ctx):
        await ctx.send(content=f'Current latency: {self.bot.latency*1000}ms')


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
