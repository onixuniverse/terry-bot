from discord.ext.commands import Cog, command, is_owner

from .. import db


class GuildHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='addguild', hidden=True)
    @is_owner()
    async def add_guild_to_db(self, ctx):
        """Ручное добавление сервера в бд"""
        results = await db.record('SELECT * FROM configs WHERE guild_id = %s', ctx.guild.id)

        if not results:
            await db.execute('INSERT INTO configs (guild_id, logging, guest, abuse) VALUES(%s, %s, %s, %s)',
                             ctx.guild.id, 'off', 'off', 'off')
            await db.execute('INSERT INTO channels (guild_id) VALUES(%s)', ctx.guild.id)
            await db.execute('INSERT INTO roles (guild_id) VALUES(%s)', ctx.guild.id)
            await db.commit()
        elif results:
            await ctx.send(f'{ctx.message.author.mention}, данный сервер уже зарегистрирован в базе данных бота.')

    @Cog.listener()
    async def on_guild_join(self, guild):
        """Автоматическое добавление сервера в бд"""
        results = await db.record('SELECT * FROM configs WHERE guild_id = %s', guild.id)

        if not results:
            await db.execute('INSERT INTO configs (guild_id, logging, guest, abuse) VALUES(%s, %s, %s, %s)',
                             guild.id, 'off', 'off', 'off')
            await db.execute('INSERT INTO channels (guild_id) VALUES(%s)', guild.id)
            await db.execute('INSERT INTO roles (guild_id) VALUES(%s)', guild.id)
            await db.commit()


def setup(bot):
    bot.add_cog(GuildHandler(bot))
