from typing import Text
from discord import channel
from loguru import logger
from discord import Embed, TextChannel
from discord.ext.commands import Cog, group
from discord.ext.commands.core import bot_has_permissions, has_permissions

from .. import db
from ..src.config import PREFIX
from ..utils import get_channel


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
                        description=f'`{PREFIX}settings <настройка>` - для подробной информации.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [(':newspaper: Логирование', f'```{PREFIX}settings logging```', False),
                      (':detective: Система "Гость"', f'```{PREFIX}settings guest```', False),
                      (':a: Система "Антимат"', f'```{PREFIX}settings abuse```', False),
                      (':loudspeaker: Каналы', f'```{PREFIX}settings channel```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
            
            await ctx.channel.send(embed=emb)

    @send_settings.command(name='logging',
                           aliases=['log', 'logger'])
    @has_permissions(manage_guild=True,
                     manage_messages=True)
    async def logging_system(self, ctx, mode=None):
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            try:
                if mode != status:
                    await db.execute('UPDATE configs SET logging = %s WHERE guild_id = %s', mode, ctx.guild.id)
                    await db.commit()
                    
                emb = Embed(color=0x6b32a8,
                            title=':newspaper: __Логирование__')
                emb.add_field(name='Установлен новый режим', value=f'`{mode}`')
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                
                await ctx.send(embed=emb)
            except Exception as err:
                logger.error(err)
                await ctx.send('[E] | Что-то пошло не так!')
        else:
            emb = Embed(color=0x6b32a8,
                        title='Настройки – :newspaper: __Логирование__',
                        description='Отправляет информацию о новых пользователях, тех, кто вышел с сервера, банах и тд.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings logging <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @send_settings.command(name='guest')
    @has_permissions(manage_guild=True,
                     manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def guest_system(self, ctx, mode=None):
        status = await db.record('SELECT guest FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            try:
                if mode != status:
                    await db.execute('UPDATE configs SET guest = %s WHERE guild_id = %s', mode, ctx.guild.id)
                    await db.commit()
                    
                emb = Embed(color=0x6b32a8,
                            title=':detective: __Система "Гость"__')
                emb.add_field(name='Установлен новый режим', value=f'`{mode}`')
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                
                await ctx.send(embed=emb)
            except Exception as err:
                logger.error(err)
                await ctx.send('[E] | Что-то пошло не так!')
        else:
            emb = Embed(color=0x6b32a8,
                        title='Настройки – :detective: __Система "Гость"__',
                        description='Выдаёт заданную роль для новых пользователей.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings guest <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @send_settings.command(name='abuse')
    @has_permissions(manage_guild=True,
                     manage_messages=True)
    async def abuse_system(self, ctx, mode=None):
        status = await db.record('SELECT abuse FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            try:
                if mode != status:
                    await db.execute('UPDATE configs SET abuse = %s WHERE guild_id = %s', mode, ctx.guild.id)
                    await db.commit()
                    
                emb = Embed(color=0x6b32a8,
                            title=':a: Система "Антимат"')
                emb.add_field(name='Установлен новый режим', value=f'`{mode}`')
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                
                await ctx.send(embed=emb)
            except Exception as err:
                logger.error(err)
                await ctx.send('[E] | Что-то пошло не так!')
        else:
            emb = Embed(color=0x6b32a8,
                        title='Настройки – :a: Система "Антимат"',
                        description='Система оповещает, если находит маты в сообщениях пользователей. (beta)')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings abuse <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)

    @send_settings.group(name='channel',
                           aliases=['channels', 'ch', 'chan'])
    @has_permissions(manage_channels=True,
                     manage_messages=True)
    async def channel_system(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** – :loudspeaker: __Каналы__',
                        description='Настройка каналов для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Для изменения канала логирования', f'```{PREFIX}settings channel log```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @channel_system.command()
    @has_permissions(manage_channels=True,
                     manage_messages=True)
    async def log(self, ctx, channel: TextChannel=None):
        channel_db = await get_channel(ctx.guild.id)
        if channel:
            try:
                if channel.id != channel_db.id:
                    await db.execute('UPDATE channels SET log_ch = %s WHERE guild_id = %s', channel.id, ctx.guild.id)
                    await db.commit()
                    
                emb = Embed(color=0x6b32a8,
                            title=':loudspeaker: __Каналы__ – :newspaper: __Логирование__')
                emb.add_field(name='Установлен новый канал логирования', value=channel.mention)
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                
                await ctx.send(embed=emb)
            except Exception as err:
                logger.error(err)
                await ctx.send('[E] | Что-то пошло не так!')
            
        else:
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** – :loudspeaker: __Каналы__ - :newspaper: __Логирование__',
                        description='Настройка канала логирования для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий канал логирования', channel_db.mention, False),
                      ('Для изменения канала логирования', f'```{PREFIX}settings channel log <#канал/ID>```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Settings(bot))
