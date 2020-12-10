from utils.roles import get_guest_role
from discord.ext.commands import Cog

from db import db


class Guesting(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        guest_status = await db.record('SELECT guest FROM configs WHERE '
                                       'guild_id = %s', member.guild.id)

        if guest_status:
            role = await get_guest_role(member.guild.id)
            if role:
                reason = 'Роль выдана системой "Гости"'

                await member.add_roles(role, reason=reason)


def setup(bot):
    bot.add_cog(Guesting(bot))
