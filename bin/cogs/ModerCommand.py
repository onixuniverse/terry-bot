from typing import Optional

from discord import Embed, Member, Role, Forbidden, HTTPException
from discord.ext.commands import Cog, Greedy, bot_has_permissions, command, has_permissions, group

from ..utils import get_channel


class ModerCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='say', brief='Повторяет текст')
    @has_permissions(send_messages=True, manage_messages=True)
    async def say_given_text(self, ctx, *, text: str):
        """Отправляет данный текст
        `[text]`: отправляемый текст"""

        if text:
            await ctx.send(text)
        else:
            await ctx.send('**[E]** | Нет подходящего текста для отправки.')

    @command(name='sayemb', brief='Текст в виде врезки')
    @has_permissions(send_messages=True, manage_messages=True)
    async def say_given_text_as_embed(self, ctx, *, text: str):
        """Отправляет данный текст в виде врезки
        `[text]`: отправляемый текст"""

        if text:
            emb = Embed(color=ctx.author.color)
            emb.description = text
            await ctx.send(embed=emb)
        else:
            await ctx.send('**[E]** | Нет подходящего текста для отправки.')

    @command(name='kick', brief='Кик учистника')
    @has_permissions(kick_members=True)
    async def kick_member(self, ctx, members: Greedy[Member], *, reason: Optional[str]):
        """Кикает пользователя

        `[members]`: пользователи
        `<reason>`: причина кика`"""

        channel = await get_channel(ctx.guild.id)

        for user in members:
            await user.kick(reason=reason)

            emb = Embed(color=0x19BCB0)
            emb.title = '**Пользователь кикнут командой**'
            fields = [('Пользователь', user.mention, True),
                      ('Никнейм', user, True),
                      ('Причина', reason, False)]

            for name, value, inline in fields:
                emb.add_field(name=name, value=value, inline=inline)

            await channel.send(embed=emb)

    @command(name='ban', brief='Бан пользователя')
    @has_permissions(ban_members=True)
    async def ban_member(self, ctx, users: Greedy[Member], *, reason: Optional[str]):
        """Банит пользователя

        `[users]`: пользователи
        `<reason>`: причина бана`"""

        for elem in users:
            await elem.ban(reason=reason)

    @command(name='clear', aliases=['purge'], brief='Удаление сообщений')
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member], count: Optional[int] = 1):
        """Удаляет указанное число сообщений(count)

        `<targets>`: пользователи от которых нужно удалить сообщения
        `<count>`: количество удаляемых сообщений. По умолчанию: 1"""

        def _check(message):
            return not len(targets) or message.author in targets

        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=count, check=_check)
        await ctx.send(f'{len(deleted):,} сообщений было удалено.', delete_after=5)

    @command(name='addrole', aliases=['giverole'], brief='Выдача ролей')
    @has_permissions(manage_roles=True)
    async def give_role(self, ctx, members: Greedy[Member], roles: Greedy[Role]):
        """Выдаёт роли указанным пользователям

        `[members]`: пользователи
        `[roles]`: роли"""

        if members:
            try:
                for elem in members:
                    await elem.add_roles(*roles)

                await ctx.send(f'Роли выданы {len(members)} участникам.')
            except Forbidden:
                await ctx.send(':x: | Нет прав на выдачу этих ролей.')
            except HTTPException:
                await ctx.send(':x: | Не удалось добавить роли.')


def setup(bot):
    bot.add_cog(ModerCommand(bot))
