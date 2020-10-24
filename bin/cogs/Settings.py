from loguru import logger
from discord import Embed, TextChannel, Role
from discord.ext.commands import Cog, group
from discord.ext.commands.core import bot_has_permissions, has_permissions

from .. import db
from data.config import PREFIX
from ..utils import get_channel, get_guest_role


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @group(name='settings',
           aliases=['setting', 'options', 'option'])
    @has_permissions(manage_messages=True)
    async def get_settings(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='Настройки',
                        description=f'`{PREFIX}settings <настройка>` - для подробной информации.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [(':newspaper: Логирование', f'```{PREFIX}settings logging```', False),
                      (':detective: Система "Гость"', f'```{PREFIX}settings guest```', False),
                      (':a: Система "Антимат"', f'```{PREFIX}settings abuse```', False),
                      (':loudspeaker: Каналы', f'```{PREFIX}settings channel```', False),
                      (':scroll: Роли', f'```{PREFIX}settings role```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
            
            await ctx.channel.send(embed=emb)

    @get_settings.command(name='logging',
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
                await ctx.send('**[E]** | Что-то пошло не так!')
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
            
    @get_settings.command(name='guest')
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
            
    @get_settings.command(name='abuse')
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
                await ctx.send('**[E]** | Что-то пошло не так!')
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

    @get_settings.group(name='channel',
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
            
    @channel_system.command(name='log',
                            aliases=['logging', 'logger'])
    @has_permissions(manage_channels=True,
                     manage_messages=True)
    async def log_channel(self, ctx, channel: TextChannel=None):
        channel_db = await get_channel(ctx.guild.id)
        
        try:
            channel_db_id = channel_db.id
        except:
            channel_db_id = None
            
        if channel:
            try:
                if channel.id != channel_db_id:
                    await db.execute('UPDATE channels SET log_ch = %s WHERE guild_id = %s', channel.id, ctx.guild.id)
                    await db.commit()
                    
                    emb = Embed(color=0x6b32a8,
                                title=':loudspeaker: __Каналы__ – :newspaper: __Логирование__')
                    emb.add_field(name='Установлен новый канал логирования', value=channel.mention)
                    emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                    
                    await ctx.send(embed=emb)
            except Exception as err:
                logger.error(err)
                await ctx.send('**[E]** | Что-то пошло не так!')
            
        else:
            try:
                channel_db_mention = channel_db.mention
            except:
                channel_db_mention = None
                
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** – :loudspeaker: __Каналы__ - :newspaper: __Логирование__',
                        description='Настройка канала логирования для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий канал логирования', channel_db_mention, False),
                      ('Для изменения канала логирования', f'```{PREFIX}settings channel log <#канал/ID>```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)

    @get_settings.group(name='role',
           aliases=['roles'])
    async def role_system(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** – :scroll: Роли',
                        description='Настройка ролей для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Для изменения роли гостя', f'```{PREFIX}settings role guest```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @role_system.command(name='guest',
                         aliases=['guests'])
    async def guest(self, ctx, role: Role=None):
        role_db = await get_guest_role(ctx.guild.id)
         
        try:
            role_db_id = role_db.id
        except:
            role_db_id = None
            
        if role:
            try:
                if role.id != role_db_id:
                    await db.execute('UPDATE roles SET guest_role = %s WHERE guild_id = %s', role.id, ctx.guild.id)
                    await db.commit()
                    
                    emb = Embed(color=0x6b32a8,
                                title=':scroll: __Роли__ – :detective: Система "Гость"')
                    emb.add_field(name='Установлена новая роль гостя', value=role.mention)
                    emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                    
                    await ctx.send(embed=emb)
            except Exception as err:
                logger.error(err)
                await ctx.send('**[E]** | Что-то пошло не так!')
            
        else:
            try:
                role_db_mention = role_db.mention
            except:
                role_db_mention = None
                
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** – :scroll: __Роли__ - :detective: Система "Гость"',
                        description='Настройка роли гостя для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущая роль гостя', role_db_mention, False),
                    ('Для изменения роли гостя', f'```{PREFIX}settings role guest <@роль/ID>```', False)]
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Settings(bot))
