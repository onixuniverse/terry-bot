from typing import Optional

from discord import Embed
from discord.ext.commands import Cog, command
from discord.utils import get
from resources.data.config import PREFIX


def syntax(command):
    cmd_aliases = '|'.join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ('self', 'ctx'):
            params.append(f'<{key}>' if 'NoneType' in str(value) else f'[{key}]')

    params = ' '.join(params)

    return (f'`{PREFIX}{cmd_aliases} {params}`')


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f'Помощь по команде `{command}`',
                      description=syntax(command), color=ctx.author.color)
        embed.add_field(name='Опиание команды', value=command.help)
        await ctx.send(embed=embed)

    @command(name='help', brief='Помощь')
    async def show_help(self, ctx, cmd: Optional[str]):
        """Показывает это сообщение"""
        if cmd:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send(f'{ctx.author.mention}, команды {command} не существует!')
        else:
            commands = self.bot.commands
            fields = []

            for cmd in commands:
                if cmd.hidden is False:
                    fields.append((cmd.brief or 'Нет краткого описания',
                                   syntax(cmd)))

            embed = Embed(title='Помощь',
                          description='Помощь по командам {self.bot.user.name}',
                          color=ctx.author.color)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text='[] - обязательный аргумент команды, <> - необязательный аргумент команды')

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
