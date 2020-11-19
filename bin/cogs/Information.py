from discord import Embed
from discord.ext.commands import Cog, command


class Information(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command(name='info', brief='Информация о боте')
    async def send_info(self, ctx):
        """Информация о боте"""
        embed = Embed(title='Информация о боте', color=ctx.author.color)
        embed.set_thumbnail(self.bot.user.avatar_url)
        
        fields = [('Имя', self.bot.user.name, True),
                  ('ID', self.bot.user.id, True),
                  ('Создатели', 'o n i x#0001', True),
                  ('Создан', self.bot.user.created_at, True),
                  ('', '', True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Information(bot))
