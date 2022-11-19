from typing import Optional

from nextcord import Embed, slash_command, Interaction
from nextcord.ext.commands import Cog
from nextcord.utils import get


def syntax(cmd, command_prefix):
    cmd_aliases = "|".join([str(cmd), *cmd.aliases])
    params = []

    for key, value in cmd.params.items():
        if key not in ("self", "ctx"):
            params.append(f"<{key}>" if "NoneType" in str(value) else f'[{key}]')

    params = " ".join(params)

    return f"`{command_prefix}{cmd_aliases} {params}`"


async def cmd_help(interaction, cmd, command_prefix):
    embed = Embed(title=f"Помощь по команде `{cmd}`", description=syntax(cmd, command_prefix),
                  color=interaction.user.color)
    embed.add_field(name="Описание команды", value=cmd.help)
    await interaction.send(embed=embed)


class HelpHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="help", force_global=True)
    async def show_help(self, interaction: Interaction, cmd: Optional[str]):
        """Помощь по командам бота."""
        if cmd:
            if cmd := get(self.bot.commands, name=cmd):
                await cmd_help(interaction, cmd, self.bot.command_prefix)
            else:
                await interaction.send(f"Команды {cmd} не существует!")
        else:
            commands = self.bot.commands
            fields = []

            for cmd in commands:
                if cmd.hidden is False:
                    fields.append((cmd.brief or "Нет краткого описания", syntax(cmd, self.bot.command_prefix)))

            embed = Embed(title=f"Помощь по командам {self.bot.user.name}", color=interaction.user.color)
            embed.set_thumbnail(url=interaction.guild.me.avatar.url)
            embed.set_footer(text="[] - обязательный аргумент команды, <> - необязательный аргумент команды, | - или")

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpHandler(bot))
