from nextcord.ext.commands import Cog, command, is_owner

from utils.configs import read_all_config, write_config


class GuildHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='addguild', hidden=True)
    @is_owner()
    async def add_guild(self, ctx):
        """Ручное добавление сервера в конфиг-файл"""
        results = read_all_config(ctx.guild.id)

        if not results:
            write_config(ctx.guild.id, "False", "False", "False")
        elif results:
            await ctx.send(f'{ctx.message.author.mention}, данный сервер уже зарегистрирован в базе данных бота.')

    @Cog.listener()
    async def on_guild_join(self, guild):
        """Автоматическое добавление сервера в бд"""
        results = read_all_config(guild.id)

        if not results:
            write_config(guild.id, "False", "False", "False")


def setup(bot):
    bot.add_cog(GuildHandler(bot))
