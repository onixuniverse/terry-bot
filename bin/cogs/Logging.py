from discord.ext.commands import Cog, command


class Logging(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_member_join(self, member):
        pass
    
    @Cog.listener()
    async def on_member_remove(self, member):
        pass
    
    @Cog.listener()
    async def on_member_ban(self, member):
        pass
    
    @Cog.listener()
    async def on_member_unban(self, member):
        pass


def setup(bot):
    bot.add_cog(Logging(bot))
