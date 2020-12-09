from discord import Member, Role, Guild
from discord.ext.commands import BucketType, Cog, cooldown, command
from random import choice
from typing import Optional


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='hug', brief='Обнимашки')
    @cooldown(1, 5, BucketType.user)
    async def hugs(self, ctx, member: Member):
        """Обнимает пользователя

        `[member]`: пользователь"""

        if ctx.message.author is not member:
            await ctx.send(f'**:hugging: | {ctx.message.author.mention} '
                           'обнял(а) {member.mention}**')

    @command(name='rand', aliases=['random', 'choice', 'выбрать', 'выбери'])
    async def random_member(self, ctx, role: Optional[Role]):
        """Выбирает одного пользователя из всех. Если не указана роль, то
        выберет из всех пользователей

        `[role]`: роль"""

        async def get_random_member(role):
            members = role.members
            try:
                result = choice(members)
            except IndexError:
                await ctx.send(f'**[E]** | {ctx.author.mention}, пользователи '
                               'не найдены.')
            return result.mention or None

        if role:
            member = await get_random_member(role)
        elif not role:
            member = await get_random_member(role=Guild.default_role)

        answers = [f'Было очень сложно, но я выбираю тебя: {member}',
                   f'Я думаю, что ты подойдешь: {member}',
                   f'{member}, я вызываю тебя!']
        answer = choice(answers)
        await ctx.send(answer)


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
