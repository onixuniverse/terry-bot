from discord import Embed
from discord.ext.commands import Cog, command, group
from discord.ext.commands.core import has_permissions

from .. import db
from ..src.config import PREFIX


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @group(name='settings',
           aliases=['setting', 'options', 'option'])
    @has_permissions(manage_messages=True)
    async def send_settings(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='Настройки',
                        description='')
            fields = [(':newspaper: Логирование', f'```{PREFIX}settings logging```', True)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
            
            await ctx.channel.send(embed=emb)

    @send_settings.command()
    @has_permissions(manage_guild=True)
    async def logging(self, ctx, mode=None):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            if mode != status:
                await db.execute('UPDATE configs SET logging = %s WHERE guild_id = %s', mode, ctx.guild.id)
                await db.commit()
        else:
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** - :newspaper: __Логирование__',
                        description='Отправляет информацию о новых пользователях, тех, кто вышел с сервера, банах и тд.')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings logging <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Settings(bot))
