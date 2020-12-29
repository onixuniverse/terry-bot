from random import choice

from discord import Role
from discord.ext.commands import Cog, Greedy, command


class SimpleCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='rand', aliases=['random', 'choice', 'выбрать'],
             brief='Выбирает одного пользователя из всех.')
    async def random_member(self, ctx, roles: Greedy[Role], quantity: int = 1):
        """Выбирает одного пользователя из всех. Если не указана роль, то
        выберет из всех пользователей
        `[roles]`: роли
        `<quantity>: количество пользователей, по умолчанию - 1`"""

        async def get_random_members(roles):
            result = []
            for role in roles:
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
            for _ in range(quantity):
                random_member = choice(members_raw)
                members_raw.remove(random_member)
                members.append(random_member)

            if quantity == 1:
                await ctx.send(f'{members[0]} - отличный вариант.')
            else:
                await ctx.send('Я выбираю их: ' + ', '.join(members))
        else:
            await ctx.send(ctx.author.mention, 'в данных ролях пользователей не найдено.')


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
