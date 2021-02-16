from discord.ext.commands import Cog


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
