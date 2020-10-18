from discord.ext.commands import Cog, command


class Cog(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='function')
    async def func(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Cog(bot))
