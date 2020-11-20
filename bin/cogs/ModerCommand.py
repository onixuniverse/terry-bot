from typing import Optional

from bin.utils.channels import get_channel
from discord import Embed, Member, Role
from discord.ext.commands import (Cog, Greedy, bot_has_permissions, command,
                                  has_permissions)


class ModerCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='say', brief='Повторяет текст')
    @has_permissions(send_messages=True, manage_messages=True)
    @bot_has_permissions(send_messages=True, manage_messages=True)
    async def say_given_text(self, ctx, *, text: str):
        """Отправляет данный текст
        `[text]`: отправляемый текст"""

        if text:
            await ctx.send(text)
        else:
            await ctx.send('**[E]** | Нет подходящего текста для отправки.')

    @command(name='sayembed', aliases=['sayemb'],
             brief='Текст в виде врезки')
    @has_permissions(send_messages=True, manage_messages=True)
    @bot_has_permissions(send_messages=True, manage_messages=True)
    async def say_given_text_as_embed(self, ctx, *, text: str):
        """Отправляет данный текст в виде врезки
        `[text]`: отправяемый текст"""

        if text:
            emb = Embed(color=ctx.author.color)
            emb.description = text
            await ctx.send(embed=emb)
        else:
            await ctx.send('**[E]** | Нет подходящего текста для отправки.')

    @command(name='kick', brief='Кик учистника')
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    async def kick_member(self, ctx, members: Greedy[Member], *,
                          reason: Optional[str] = 'Нет видимой причины'):
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
    @bot_has_permissions(ban_members=True)
    async def ban_member(self, ctx, users: Greedy[Member], *,
                         reason: Optional[str] = 'Нет видимой причины.'):
        """Банит пользователя
        
        `[users]`: пользователи
        `<reason>`: причина бана`"""

        for user in users:
            await user.ban(reason=reason)

    @command(name='clear', aliases=['purge'], brief='Удаление сообщений')
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member],
                             count: Optional[int] = 1):
        """Удалет указаное число сообщений(count)

        `<targets>`: пользоватли от которых нужно удалить сообщения
        `<count>`: количество удаляемых сообщений. По умолчанию: 1"""

        def _check(message):
            return not len(targets) or message.author in targets

        with ctx.channel.typing():
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=count, check=_check)
            await ctx.send(f'{len(deleted):,} сообщений было удалено.',
                           delete_after=5)

    @command(name='addrole', brief='Выдача ролей')
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def give_role(self, ctx, member: Greedy[Member],
                        roles: Greedy[Role]):
        """Выдаёт роли указанным ползователям

        `[member]`: пользователи
        `[roles]`: роли"""
        await member.add_roles(*roles, reason=f'Выдана: {ctx.message.author}')


def setup(bot):
    bot.add_cog(ModerCommand(bot))
