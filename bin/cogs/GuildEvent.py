from discord.ext.commands import Cog, command


class GuildEvent(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
        
def setup(bot):
    bot.add_cog(GuildEvent(bot))
