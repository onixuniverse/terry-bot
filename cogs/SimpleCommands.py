from nextcord import slash_command, Interaction
from nextcord.ext.commands import Cog, command


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(force_global=True)
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency*1000)}ms")


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
