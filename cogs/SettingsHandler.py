from typing import Optional

from nextcord import Embed, Role, TextChannel
from nextcord.ext.commands import (Cog, bot_has_permissions, group, has_permissions)

from utils.channels import get_channel
from utils.configs import read_config, rewrite_config
from utils.roles import get_role


def create_settings_embed(title: str, status: str, prefix):
    embed = Embed(color=0x6b32a8,
                  title=f'**Настройки** – {title}')
    embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

    fields = [('Текущий режим', f'`{status}`', False),
              ('Доступные режимы', '`True/False`', False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


class SettingsHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(name='settings', aliases=['options'], brief='Настройки бота.')
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def send_settings(self, ctx):
        """Доступные настройки бота"""

        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8, title='**Настройки**',
                        description=f'`{self.bot.command_prefix}settings <настройка>` - '
                                    'для подробной информации.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

            fields = [(':newspaper: __Логирование__', f'```{self.bot.command_prefix}settings logging```'),
                      (':detective: __Система "Гость"__', f'```{self.bot.command_prefix}settings guest```'),
                      (':a: __Система "Антимат"__', f'```{self.bot.command_prefix}settings abuse```'),
                      (':loudspeaker: __Каналы__', f'```{self.bot.command_prefix}settings channel```'),
                      (':scroll: __Роли__', f'```{self.bot.command_prefix}settings role```')]

            for name, value in fields:
                emb.add_field(name=name, value=value, inline=False)

            await ctx.channel.send(embed=emb)

    @send_settings.command(name='logging', aliases=['log', 'logger'])
    @has_permissions(manage_guild=True, manage_messages=True)
    @bot_has_permissions(manage_guild=True, manage_messages=True)
    async def on_logging(self, ctx, mode: Optional[str]):
        title = ':newspaper: __Логирование__'

        status = read_config(ctx.guild.id, "log_mode")

        if mode == 'True' or mode == 'False':
            if mode != status:
                rewrite_config(ctx.guild.id, "log_mode", mode)

                await ctx.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
            else:
                await ctx.send(f':x: | Режим `{mode}` для {title} уже установлен.')
        else:
            embed = create_settings_embed(title, status, self.bot.command_prefix)
            embed.description = "Отправляет информацию о новых пользователях, вход/выход, бан/разбан и тд."
            embed.add_field(name="Для изменения режима", value=f"{self.bot.command_prefix}settings logging <режим>",
                            inline=False)

            await ctx.send(embed=embed)

    @send_settings.command(name='guest')
    @has_permissions(manage_guild=True, manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def on_guesting(self, ctx, mode: Optional[str]):
        title = ':detective: __Система "Гость"__'

        status = read_config(ctx.guild.id, "guest_mode")

        if mode == 'True' or mode == 'False':
            if mode != status:
                rewrite_config(ctx.guild.id, "guest_mode", mode)

                await ctx.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
            else:
                await ctx.send(f':x: | Режим `{mode}` для {title} уже установлен.')

        else:
            embed = create_settings_embed(title, status, self.bot.command_prefix)
            embed.description = "Выдаёт заданную роль для новых пользователей."
            embed.add_field(name="Для изменения режима", value=f"{self.bot.command_prefix}settings guest <режим>",
                            inline=False)

            await ctx.send(embed=embed)

    @send_settings.command(name='abuse')
    @has_permissions(manage_guild=True, manage_messages=True)
    @bot_has_permissions(manage_guild=True, manage_messages=True)
    async def on_abusing(self, ctx, mode: Optional[str]):
        title = ':a: __Система "Антимат"__'

        status = read_config(ctx.guild.id, "guest_mode")

        if mode == 'True' or mode == 'False':
            if mode != status:
                rewrite_config(ctx.guild.id, "abuse_mode", mode)

                await ctx.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')

            else:
                await ctx.send(f':x: | Режим `{mode}` для {title} уже установлен.')

        else:
            embed = create_settings_embed(title, status, self.bot.command_prefix)
            embed.description = "Система оповещает, если находит маты в сообщениях пользователей."
            embed.add_field(name="Для изменения режима", value=f"{self.bot.command_prefix}settings abuse <режим>",
                            inline=False)

            await ctx.send(embed=embed)

    @send_settings.group(name='channel')
    @has_permissions(manage_channels=True, manage_messages=True)
    @bot_has_permissions(manage_channels=True, manage_messages=True)
    async def channel_system(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8, title='**Настройки** – :loudspeaker: __Каналы__',
                        description='Настройка каналов для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            emb.add_field(name='Для изменения канала логирования', value=f'```{self.bot.command_prefix}settings channel log```',
                          inline=False)

            await ctx.send(embed=emb)

    @channel_system.command(name='log', aliases=['logging', 'logger'])
    @has_permissions(manage_channels=True, manage_messages=True)
    @bot_has_permissions(manage_channels=True, manage_messages=True)
    async def log_channel(self, ctx, channel: Optional[TextChannel]):
        channel_db = await get_channel(self.bot, ctx.guild.id, "log_channel_id")

        title = ':newspaper: __Логирование__'

        if channel:
            channel_db_id = channel_db.id if channel_db else None
            if channel.id != channel_db_id:
                rewrite_config(ctx.guild.id, "log_channel_id", str(channel.id))

                embed = Embed(color=0x6b32a8, title=f':loudspeaker: __Каналы__ – {title}')
                embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                embed.add_field(name='Установлен новый канал логирования', value=channel.mention)

                await ctx.send(embed=embed)
        else:
            channel_db_mention = channel_db.mention if channel_db else None

            embed = Embed(color=0x6b32a8, title=f'**Настройки** – {title} - :newspaper: __Логирование__',
                          description='Настройка канала логирования для данного сервера.')
            embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

            fields = [('Текущий канал логирования', channel_db_mention, False),
                      ('Для изменения канала логирования',
                       f'```{self.bot.command_prefix}settings channel log <#канал/ID>```', False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

    @send_settings.group(name='role', aliases=["roles"])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def role_system(self, ctx):
        if not ctx.invoked_subcommand:
            emb = Embed(color=0x6b32a8, title='**Настройки** – :scroll: Роли',
                        description='Настройка ролей для данного сервера.')
            emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
            emb.add_field(name='Для изменения роли гостя', value=f'```{self.bot.command_prefix}settings role guest```',
                          inline=False)

            await ctx.send(embed=emb)

    @role_system.command(name='guest', aliases=['guests'])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def guest(self, ctx, role: Optional[Role]):
        guest_role = await get_role(self.bot, ctx.guild.id, 'guest_role_id')

        if role:
            guest_role_id = guest_role.id if guest_role else None

            if role.id != guest_role_id:
                rewrite_config(ctx.guild.id, "guest_role_id", str(role.id))

                embed = Embed(color=0x6b32a8, title=':scroll: __Роли__ – :detective: __Система "Гость"__')
                embed.add_field(name='Установлена новая роль', value=role.mention)
                embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

                await ctx.send(embed=embed)
        else:
            role_db_mention = guest_role.mention if guest_role else None

            embed = Embed(color=0x6b32a8, title='**Настройки** – :scroll: __Роли__ - :detective: __Система "Гость"__',
                          description='Настройка роли гостя для данного сервера.')
            embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

            fields = [('Текущая роль', role_db_mention, False),
                      ('Для изменения роли', f'```{self.bot.command_prefix}settings role guest <@роль/ID>```', False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SettingsHandler(bot))
