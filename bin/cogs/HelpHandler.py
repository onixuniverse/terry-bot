from discord.ext.commands import Cog


class HelpHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    


def setup(bot):
    bot.add_cog(HelpHandler(bot))
