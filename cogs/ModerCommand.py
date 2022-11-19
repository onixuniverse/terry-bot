from random import choice
from typing import Optional

from nextcord import Embed, Member, Role, Forbidden, HTTPException
from nextcord.ext.commands import Cog, Greedy, command, has_permissions


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

    @command(name='random', aliases=['choice'], brief='Выбирает одного пользователя из всех.')
    @has_permissions(manage_roles=True)
    async def random_member(self, ctx, roles: Greedy[Role], quantity: int = 1):
        """Выбирает одного или нескольких пользователей из всех. Если не указана роль, то
        выберет из всех пользователей
        `[roles]`: роли
        `<quantity>`: количество пользователей, по умолчанию - 1"""

        async def get_random_members(member_roles):
            result = []
            for role in member_roles:
                try:
                    for member in role.members:
                        result.append(member.mention)
                except IndexError:
                    pass

            return result

        if roles:
            members_raw = await get_random_members(roles)
        else:
            members_raw = await get_random_members([ctx.guild.default_role])

        if members_raw:
            members = []
            try:
                for _ in range(quantity):
                    random_member = choice(members_raw)
                    members_raw.remove(random_member)
                    members.append(random_member)
            except IndexError:
                pass

            if quantity == 1:
                await ctx.send(f'{members[0]} - отличный вариант.')
            else:
                await ctx.send('Я выбираю их: ' + ', '.join(members))
        else:
            await ctx.send(ctx.author.mention, 'в данных ролях пользователей не найдено.')


def setup(bot):
    bot.add_cog(ModerCommand(bot))
