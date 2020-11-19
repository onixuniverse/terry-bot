from typing import Optional

from discord import Embed, Role, TextChannel
from discord.ext.commands import (Cog, bot_has_permissions, group,
                                  has_permissions)
from loguru import logger
from resources.data.config import PREFIX

from .. import db
from ..utils import get_channel, get_curator_role, get_guest_role


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @group(name='settings', aliases=['options'], brief='Настройки бота.')
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def send_settings(self, ctx):
        """Доступные настройки бота"""
        
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='**Настройки**',
                        description=f'`{PREFIX}settings <настройка>` - для подробной информации.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            
            fields = [(':newspaper: __Логирование__', f'```{PREFIX}settings logging```'),
                      (':detective: __Система "Гость"__', f'```{PREFIX}settings guest```'),
                      (':a: __Система "Антимат"__', f'```{PREFIX}settings abuse```'),
                      (':loudspeaker: __Каналы__', f'```{PREFIX}settings channel```'),
                      (':scroll: __Роли__', f'```{PREFIX}settings role```'),
                      (':dvd: __Электронная таблица__', f'```{PREFIX}spreadsheet```')]
            
            for name, value in fields:
                emb.add_field(name=name, value=value, inline=False)
            
            await ctx.channel.send(embed=emb)

    @send_settings.command(name='logging', aliases=['log', 'logger'])
    @has_permissions(manage_guild=True, manage_messages=True)
    @bot_has_permissions(manage_guild=True, manage_messages=True)
    async def logging_system(self, ctx, mode: Optional[str]):
        title = ':newspaper: __Логирование__'
        
        status = await db.record('SELECT logging FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            try:
                if mode != status:
                    await db.execute('UPDATE configs SET logging = %s WHERE guild_id = %s', mode, ctx.guild.id)
                    await db.commit()
                    
                    await ctx.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
                else:
                    await ctx.send(f':x: | Режим `{mode}` для {title} уже установлен.')
            except Exception as exc:
                logger.error(exc)
        else:
            emb = Embed(color=0x6b32a8,
                        title=f'**Настройки** – {title}',
                        description='Отправляет информацию о новых пользователях, тех, кто вышел с сервера, банах и тд.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings logging <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @send_settings.command(name='guest')
    @has_permissions(manage_guild=True, manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def guest_system(self, ctx, mode: Optional[str]):
        title = ':detective: __Система "Гость"__'
        
        status = await db.record('SELECT guest FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            try:
                if mode != status:
                    await db.execute('UPDATE configs SET guest = %s WHERE guild_id = %s', mode, ctx.guild.id)
                    await db.commit()
                    
                    await ctx.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
                else:
                    await ctx.send(f':x: | Режим `{mode}` для {title} уже установлен.')
            except Exception as err:
                logger.error(err)
                await ctx.send('[E] | Что-то пошло не так!')
        else:
            emb = Embed(color=0x6b32a8,
                        title=f'**Настройки** – {title}',
                        description='Выдаёт заданную роль для новых пользователей.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings guest <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @send_settings.command(name='abuse')
    @has_permissions(manage_guild=True, manage_messages=True)
    @bot_has_permissions(manage_guild=True, manage_messages=True)
    async def abuse_system(self, ctx, mode: Optional[str]):
        title = ':a: __Система "Антимат"__'
        
        status = await db.record('SELECT abuse FROM configs WHERE guild_id = %s', ctx.guild.id)
        if mode == 'on' or mode == 'off':
            try:
                if mode != status:
                    await db.execute('UPDATE configs SET abuse = %s WHERE guild_id = %s', mode, ctx.guild.id)
                    await db.commit()
                    
                    await ctx.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
                else:
                    await ctx.send(f':x: | Режим `{mode}` для {title} уже установлен.')
            except Exception as err:
                logger.error(err)
                await ctx.send('**[E]** | Что-то пошло не так!')
        else:
            emb = Embed(color=0x6b32a8,
                        title=f'**Настройки** – {title}',
                        description='Система оповещает, если находит маты в сообщениях пользователей.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий режим', f'`{status}`', False),
                      ('Для изменения режима', f'```{PREFIX}settings abuse <режим>```', False),
                      ('Доступные режимы', '`on/off`', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)

    @send_settings.group(name='channel',
                         aliases=['channels', 'ch', 'chan'])
    @has_permissions(manage_channels=True, manage_messages=True)
    @bot_has_permissions(manage_channels=True, manage_messages=True)
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
            
    @channel_system.command(name='log', aliases=['logging', 'logger'])
    @has_permissions(manage_channels=True, manage_messages=True)
    @bot_has_permissions(manage_channels=True, manage_messages=True)
    async def log_channel(self, ctx, channel: Optional[TextChannel]):
        channel_db = await get_channel(ctx.guild.id)
        
        try:
            channel_db_id = channel_db.id
        except:
            channel_db_id = None
        
        title = ':newspaper: __Логирование__'
        
        if channel:
            try:
                if channel.id != channel_db_id:
                    await db.execute('UPDATE channels SET log_ch = %s WHERE guild_id = %s', channel.id, ctx.guild.id)
                    await db.commit()
                    
                    emb = Embed(color=0x6b32a8,
                                title=f':loudspeaker: __Каналы__ – {title}')
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
                        title=f'**Настройки** – {title} - :newspaper: __Логирование__',
                        description='Настройка канала логирования для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущий канал логирования', channel_db_mention, False),
                      ('Для изменения канала логирования', f'```{PREFIX}settings channel log <#канал/ID>```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
            
            await ctx.send(embed=emb)

    @send_settings.group(name='role', aliases=['roles'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def role_system(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8,
                        title='**Настройки** – :scroll: Роли',
                        description='Настройка ролей для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Для изменения роли гостя', f'```{PREFIX}settings role guest```', False),
                      ('Для изменения роли куратора', f'```{PREFIX}settings role curator```', False)]
            
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)
            
    @role_system.command(name='guest', aliases=['guests'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def guest(self, ctx, role: Optional[Role]):
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
                                title=':scroll: __Роли__ – :detective: __Система "Гость"__')
                    emb.add_field(name='Установлена новая роль', value=role.mention)
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
                        title='**Настройки** – :scroll: __Роли__ - :detective: __Система "Гость"__',
                        description='Настройка роли гостя для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущая роль', role_db_mention, False),
                    ('Для изменения роли', f'```{PREFIX}settings role guest <@роль/ID>```', False)]
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)

    @role_system.command(name='curator', aliases=['curators'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def curator_role(self, ctx, role: Optional[Role]):
        role_db = await get_curator_role(ctx.guild.id)
         
        try:
            role_db_id = role_db.id
        except:
            role_db_id = None
            
        if role:
            try:
                if role.id != role_db_id:
                    await db.execute('UPDATE roles SET curator_role = %s WHERE guild_id = %s', role.id, ctx.guild.id)
                    await db.commit()
                    
                    emb = Embed(color=0x6b32a8,
                                title=':scroll: __Роли__ – __:man_mage: Куратор__')
                    emb.add_field(name='Установлена новая роль', value=role.mention)
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
                        title='**Настройки** – :scroll: __Роли__ - __:man_mage: Куратор__',
                        description='Настройка роли куратора для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            fields = [('Текущая роль', role_db_mention, False),
                    ('Для изменения роли', f'```{PREFIX}settings role curator <@роль/ID>```', False)]
            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)
                
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Settings(bot))
