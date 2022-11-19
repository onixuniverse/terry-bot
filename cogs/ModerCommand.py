from random import choice
from typing import Optional

from nextcord import Embed, Member, Role, Forbidden, HTTPException, slash_command, Interaction, Permissions
from nextcord.ext.commands import Cog, Greedy, command, has_permissions


class ModerCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="say", force_global=True, default_member_permissions=Permissions(manage_messages=True))
    async def say_given_text(self, interaction: Interaction, *, text: str):
        """Отправляет данный текст."""

        if text:
            await interaction.send(text)
        else:
            await interaction.send(":x: | Нет подходящего текста для отправки.")

    @slash_command(name="sayemb", default_member_permissions=Permissions(manage_messages=True))
    async def say_given_text_as_embed(self, interaction: Interaction, *, text: str):
        """Отправляет данный текст в виде врезки."""

        if text:
            emb = Embed(color=interaction.user.color)
            emb.description = text
            await interaction.send(embed=emb)
        else:
            await interaction.send(':x: | Нет подходящего текста для отправки.')

    # @slash_command(name="purge", force_global=True, default_member_permissions=Permissions(manage_messages=True))
    # async def purge_messages(self, interaction: Interaction, targets: Greedy[Member], count: Optional[int] = 1):
    #     """Удаляет указанное число сообщений."""
    #
    #     def _check(message):
    #         return not len(targets) or message.author in targets
    #
    #     await interaction.message.delete()
    #     deleted = await interaction.channel.purge(limit=count, check=_check)
    #     await interaction.send(f'{len(deleted):,} сообщений было удалено.', delete_after=5)
    #
    # @slash_command(name="addroles", force_global=True, default_member_permissions=Permissions(manage_roles=True))
    # async def give_roles(self, interaction: Interaction, members: Greedy[Member], roles: Greedy[Role]):
    #     """Выдаёт роли указанным пользователям."""
    #     if members:
    #         try:
    #             for elem in members:
    #                 await elem.add_roles(*roles)
    #
    #             await interaction.send(f'Роли выданы {len(members)} участникам.')
    #         except Forbidden:
    #             await interaction.send(':x: | Нет прав на выдачу этих ролей.')
    #         except HTTPException:
    #             await interaction.send(':x: | Не удалось добавить роли.')
    #
    # @slash_command(name="choice", force_global=True, default_member_permissions=Permissions(manage_roles=True))
    # async def choice_random_member(self, interaction: Interaction, roles: Greedy[Role], quantity: int = 1):
    #     """Выбирает одного или нескольких пользователей из всех. Если не указана роль, то
    #     выберет из всех пользователей."""
    #     async def get_random_members(member_roles):
    #         result = []
    #         for role in member_roles:
    #             try:
    #                 for member in role.members:
    #                     result.append(member.mention)
    #             except IndexError:
    #                 pass
    #
    #         return result
    #
    #     if roles:
    #         members_raw = await get_random_members(roles)
    #     else:
    #         members_raw = await get_random_members([interaction.guild.default_role])
    #
    #     if members_raw:
    #         members = []
    #         try:
    #             for _ in range(quantity):
    #                 random_member = choice(members_raw)
    #                 members_raw.remove(random_member)
    #                 members.append(random_member)
    #         except IndexError:
    #             pass
    #
    #         if quantity == 1:
    #             await interaction.send(f"{members[0]} - отличный вариант.")
    #         else:
    #             await interaction.send("Я выбираю их: " + ", ".join(members))
    #     else:
    #         await interaction.send(f":x: | В данных ролях пользователей не найдено!")


def setup(bot):
    bot.add_cog(ModerCommand(bot))
