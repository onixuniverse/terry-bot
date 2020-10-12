from discord import Embed
from discord.ext.commands import Cog, command, group

from ..bot.config import PREFIX


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @group(name='settings',
           aliases=['setting', 'options', 'option'])
    async def send_settings(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='Настройки',
                        description='')
            fields = [(':newspaper: Логирование', f'{PREFIX}settings logging', True)]
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
            
            await ctx.channel.send(embed=emb)

    @send_settings.command()
    async def logging(self, ctx, mode=None):
        if mode:
            pass
        else:
            pass


def setup(bot):
    bot.add_cog(Settings(bot))
