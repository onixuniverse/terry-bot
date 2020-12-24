from random import choice

from discord import Member, Role
from discord.ext.commands import BucketType, Cog, Greedy, command, cooldown


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

    @command(name='rand', aliases=['random', 'choice', 'выбрать', 'выбери'],
             brief='Выбирает одного пользователя из всех.')
    async def random_member(self, ctx, role: Greedy[Role]):
        """Выбирает одного пользователя из всех. Если не указана роль, то
        выберет из всех пользователей
        `[role]`: роль"""

        async def get_random_members(role):
            try:
                result = choice(role.members)
            except IndexError:
                result = None

            return result

        if role:
            member = await get_random_members(role)
        else:
            member = await get_random_members(role=ctx.guild.default_role)

        await ctx.send(f'Это лучший вариант: {member}')


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
