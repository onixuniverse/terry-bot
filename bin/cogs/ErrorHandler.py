from discord.ext.commands import Cog, command


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
