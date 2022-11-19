from typing import Optional

from nextcord import Embed, Role, TextChannel, slash_command, Interaction, Permissions
from nextcord.ext.commands import Cog

from utils.channels import get_channel
from utils.configs import read_config, rewrite_config
from utils.roles import get_role


def create_settings_embed(title: str, status: str):
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

    @slash_command(name='settings', force_global=True, default_member_permissions=Permissions(manage_messages=True))
    async def settings(self, interaction: Interaction):
        pass

    @settings.subcommand(name="list")
    async def settings_list(self, interaction: Interaction):
        """Доступные настройки бота."""
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

        await interaction.send(embed=emb)

    @settings.subcommand(name='logging')
    async def logging_setting(self, interaction: Interaction, mode: Optional[str]):
        title = ':newspaper: __Логирование__'

        status = read_config(interaction.guild.id, "log_mode")

        if mode == 'True' or mode == 'False':
            if mode != status:
                rewrite_config(interaction.guild.id, "log_mode", mode)

                await interaction.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
            else:
                await interaction.send(f':x: | Режим `{mode}` для {title} уже установлен.')
        else:
            embed = create_settings_embed(title, status)
            embed.description = "Отправляет информацию о новых пользователях, вход/выход, бан/разбан и тд."
            embed.add_field(name="Для изменения режима", value=f"{self.bot.command_prefix}settings logging <режим>",
                            inline=False)

            await interaction.send(embed=embed)

    @settings.subcommand(name='guest')
    async def guest_setting(self, interaction: Interaction, mode: Optional[str]):
        title = ':detective: __Система "Гость"__'

        status = read_config(interaction.guild.id, "guest_mode")

        if mode == 'True' or mode == 'False':
            if mode != status:
                rewrite_config(interaction.guild.id, "guest_mode", mode)

                await interaction.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')
            else:
                await interaction.send(f':x: | Режим `{mode}` для {title} уже установлен.')

        else:
            embed = create_settings_embed(title, status)
            embed.description = "Выдаёт заданную роль для новых пользователей."
            embed.add_field(name="Для изменения режима", value=f"{self.bot.command_prefix}settings guest <режим>",
                            inline=False)

            await interaction.send(embed=embed)

    @settings.subcommand(name='abuse')
    async def abusing_setting(self, interaction: Interaction, mode: Optional[str]):
        title = ':a: __Система "Антимат"__'

        status = read_config(interaction.guild.id, "guest_mode")

        if mode == 'True' or mode == 'False':
            if mode != status:
                rewrite_config(interaction.guild.id, "abuse_mode", mode)

                await interaction.send(f':white_check_mark: | Режим для {title} изменён на `{mode}`.')

            else:
                await interaction.send(f':x: | Режим `{mode}` для {title} уже установлен.')

        else:
            embed = create_settings_embed(title, status)
            embed.description = "Система оповещает, если находит маты в сообщениях пользователей."
            embed.add_field(name="Для изменения режима", value=f"{self.bot.command_prefix}settings abuse <режим>",
                            inline=False)

            await interaction.send(embed=embed)

    @settings.subcommand(name='channel')
    async def channel_system(self, interaction: Interaction):
        emb = Embed(color=0x6b32a8, title='**Настройки** – :loudspeaker: __Каналы__',
                    description='Настройка каналов для данного сервера.')
        emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
        emb.add_field(name='Для изменения канала логирования',
                      value=f'```{self.bot.command_prefix}settings channel logging```',
                      inline=False)

        await interaction.send(embed=emb)

    @channel_system.subcommand(name='logchannel')
    async def log_channel_setting(self, interaction: Interaction, channel: Optional[TextChannel]):
        channel_db = await get_channel(self.bot, interaction.guild.id, "log_channel_id")

        title = ':newspaper: __Логирование__'

        if channel:
            channel_db_id = channel_db.id if channel_db else None
            if channel.id != channel_db_id:
                rewrite_config(interaction.guild.id, "log_channel_id", str(channel.id))

                embed = Embed(color=0x6b32a8, title=f':loudspeaker: __Каналы__ – {title}')
                embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
                embed.add_field(name='Установлен новый канал логирования', value=channel.mention)

                await interaction.send(embed=embed)
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

            await interaction.send(embed=embed)

    @settings.subcommand(name='role')
    async def role_system(self, interaction: Interaction):
        emb = Embed(color=0x6b32a8, title='**Настройки** – :scroll: Роли',
                    description='Настройка ролей для данного сервера.')
        emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')
        emb.add_field(name='Для изменения роли гостя', value=f'```{self.bot.command_prefix}settings role guest```',
                      inline=False)

        await interaction.send(embed=emb)

    @role_system.subcommand(name='guest')
    async def guest_role_setting(self, interaction: Interaction, role: Optional[Role]):
        guest_role = await get_role(self.bot, interaction.guild.id, 'guest_role_id')

        if role:
            guest_role_id = guest_role.id if guest_role else None

            if role.id != guest_role_id:
                rewrite_config(interaction.guild.id, "guest_role_id", str(role.id))

                embed = Embed(color=0x6b32a8, title=':scroll: __Роли__ – :detective: __Система "Гость"__')
                embed.add_field(name='Установлена новая роль', value=role.mention)
                embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

                await interaction.send(embed=embed)
        else:
            role_db_mention = guest_role.mention if guest_role else None

            embed = Embed(color=0x6b32a8, title='**Настройки** – :scroll: __Роли__ - :detective: __Система "Гость"__',
                          description='Настройка роли гостя для данного сервера.')
            embed.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/settings.png')

            fields = [('Текущая роль', role_db_mention, False),
                      ('Для изменения роли', f'```{self.bot.command_prefix}settings role guest <@роль/ID>```', False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(SettingsHandler(bot))
