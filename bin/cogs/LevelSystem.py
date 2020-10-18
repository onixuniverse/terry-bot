from discord.ext.commands import Cog, command


class LevelSystem(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='lvl',
             aliases=['lvls', 'level', 'levels'])
    async def get_lvl(self, ctx):
        pass


def setup(bot):
    bot.add_cog(LevelSystem(bot))
