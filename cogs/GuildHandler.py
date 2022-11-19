from nextcord import slash_command, Permissions, Interaction
from nextcord.ext.commands import Cog, command

from utils.configs import read_all_config, write_config


class GuildHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="addguild", force_global=True, default_member_permissions=8)
    async def add_guild(self, interaction: Interaction):
        """Ручное добавление сервера в конфиг-файл"""
        results = read_all_config(interaction.guild.id)

        if not results:
            write_config(interaction.guild.id, "False", "False", "False")
        else:
            await interaction.response.send_message(':white_check_mark: | Данный сервер уже зарегистрирован! Отлично!')

    @Cog.listener()
    async def on_guild_join(self, guild):
        """Автоматическое добавление сервера в бд"""
        results = read_all_config(guild.id)

        if not results:
            write_config(guild.id, "False", "False", "False")


def setup(bot):
    bot.add_cog(GuildHandler(bot))
