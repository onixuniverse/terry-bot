from discord.ext.commands import Cog


class Statistics(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    pass


def setup(bot):
    bot.add_cog(Statistics(bot))