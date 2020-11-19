from discord.ext.commands import Cog, command, is_owner
from loguru import logger

from .. import db


class GuildAdding(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='addguild', hidden=True)
    @is_owner()
    async def add_guild_to_db(self, ctx):
        """Ручное добалвение сервера в базу данных"""
        results = await db.field('SELECT * FROM configs WHERE guild_id = %s', ctx.guild.id)
        
        if not results:
            await db.execute('INSERT INTO configs (guild_id, user_log, guest, abuse) VALUES(%s, %s, %s, %s)',
                            ctx.guild.id, 'off', 'off', 'off')
            await db.execute('INSERT INTO channels (guild_id) VALUES(%s)', ctx.guild.id)
            await db.execute('INSERT INTO roles (guild_id) VALUES(%s)', ctx.guild.id)
            await db.commit()
            
            logger.info(f'Added a new guild. ID: {ctx.guild.id}, Name: {ctx.guild.name}')
            
        elif results:
            await ctx.send(f'{ctx.message.author.mention}, this guild is already exist in DB.')
            
        else:
            logger.error(f'Results return: {results}')
        
    @Cog.listener()
    async def on_guild_join(self, guild):
        """Auto adding a guild to the database."""
        results = await db.field('SELECT * FROM configs WHERE guild_id = %s', guild.id)
        
        if not results:
            await db.execute('INSERT INTO configs (guild_id, user_log, guest, abuse) VALUES(%s, %s, %s, %s)',
                            guild.id, 'off', 'off', 'off')
            await db.execute('INSERT INTO channels (guild_id) VALUES(%s)', guild.id)
            await db.execute('INSERT INTO roles (guild_id) VALUES(%s)', guild.id)
            await db.commit()
            
            logger.info(f'Added a new guild. ID: {guild.id}, Name: {guild.name}')
            
        elif results:
            logger.info('Guild is already exist in DB. ID: {guild.id}, Name: {guild.name}')
            
        else:
            logger.error(f'Results return: {results}')
    
        
def setup(bot):
    bot.add_cog(GuildAdding(bot))
