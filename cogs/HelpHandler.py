from typing import Optional

from nextcord import Embed
from nextcord.ext.commands import command, Bot, Cog
from nextcord.utils import get


def syntax(cmd, command_prefix):
    cmd_aliases = '|'.join([str(cmd), *cmd.aliases])
    params = []

    for key, value in cmd.params.items():
        if key not in ('self', 'ctx'):
            params.append(f'<{key}>' if 'NoneType' in str(value) else f'[{key}]')

    params = ' '.join(params)

    return f'`{command_prefix}{cmd_aliases} {params}`'


async def cmd_help(ctx, cmd, command_prefix):
    embed = Embed(title=f'Помощь по команде `{cmd}`', description=syntax(cmd, command_prefix), color=ctx.author.color)
    embed.add_field(name='Описание команды', value=cmd.help)
    await ctx.send(embed=embed)


class HelpHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='help', brief='Помощь')
    async def show_help(self, ctx, cmd: Optional[str]):
        """Показывает это сообщение"""
        if cmd:
            if cmd := get(self.bot.commands, name=cmd):
                await cmd_help(ctx, cmd, self.bot.command_prefix)
            else:
                await ctx.send(f'{ctx.author.mention}, команды {cmd} не существует!')
        else:
            commands = self.bot.commands
            fields = []

            for cmd in commands:
                if cmd.hidden is False:
                    fields.append((cmd.brief or 'Нет краткого описания', syntax(cmd, self.bot.command_prefix)))

            embed = Embed(title=f'Помощь по командам {self.bot.user.name}', color=ctx.author.color)
            embed.set_thumbnail(url=ctx.guild.me.avatar.url)
            embed.set_footer(text='[] - обязательный аргумент команды, <> - необязательный аргумент команды, | - или')

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, msg):
        if msg.author is Bot:
            return

        if self.bot in msg.mentions:
            content = 'Привет, меня зовут Терри, я помогаю на серверах для дистанционного обучения.\n' \
                      'Чтобы узнать мои команды введи {PREFIX}help.\nК сожалению, я нахожусь ещё в стадии разработки.'

            await msg.channel.send(content, mention_author=True)


def setup(bot):
    bot.add_cog(HelpHandler(bot))
