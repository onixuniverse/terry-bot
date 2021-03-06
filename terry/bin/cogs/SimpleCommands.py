from discord.ext.commands import Cog, command


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ping(self, ctx):
        await ctx.send(content=f'Pong! {self.bot.latency*1000}ms')


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
