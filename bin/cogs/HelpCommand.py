from typing import Optional, ValuesView

from discord.ext.menus import MenuPages, ListPageSource
from discord import Embed
from discord.ext.commands import Cog, command
from discord.utils import get


def syntax(command):
    cmd_aliases = '|'.join([str(command), *command.aliases])
    params = []
    
    for key, value in command.params.items():
        if key not in ('self', 'ctx'):
            params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')
    
    params = ' '.join(params)
    
    return (f'```{cmd_aliases} {params}```')


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        
        super().__init__(data, per_page=3)
        
    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)
        
        embed = Embed(title='Помощь',
                      description='Помощь по командам Terry.',
                      color=self.ctx.author.color)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f'{offset:,} - {min(len_data, offset+self.per_page-1):,} из {len_data:,} команд.')
        
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
            
        return embed
    
    async def format_page(self, menu, entries):
        fields = []
        
        for entry in entries:
            if entry.hidden == False:
                fields.append((entry.brief or 'Нет описания', syntax(entry)))
            
        return await self.write_page(menu, fields)


class HelpCommand(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def cmd_help(self, ctx, command):
        embed = Embed(title=f'Помощь по команде `{command}`',
                      description=syntax(command),
                      color=ctx.author.color)
        embed.add_field(name='Опиание команды', value=command.help)
        await ctx.send(embed=embed)
    
    @command(name='help')
    async def show_help(self, ctx, cmd: Optional[str]):
        """Show this message."""
        if cmd:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send('Такой команды нет.')
        else:
            menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
                             delete_message_after=True,
                             timeout=60.0)
            await menu.start(ctx)
    
    
def setup(bot):
    bot.add_cog(HelpCommand(bot))
