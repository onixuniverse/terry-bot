from discord.ext.commands import Cog, command

from .. import db


class LevelSystem(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='lvl',
             aliases=['lvls', 'level', 'levels'])
    async def get_lvl(self, ctx):
        lvl = db.record('SELECT lvl FROM levels WHERE guild_id, member_id = %s, %s', ctx.guild.id, ctx.message.author.id)


def setup(bot):
    bot.add_cog(LevelSystem(bot))
