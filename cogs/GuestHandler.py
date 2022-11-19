from nextcord.ext.commands import Cog

from utils.configs import read_config
from utils.roles import get_role


class GuestHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        guest_status = read_config(member.guild.id, "guest_mode")

        if guest_status:
            role = await get_role(self.bot, member.guild.id, 'guest')
            if role:
                reason = 'Роль выдана системой "Гости" by Terry'

                await member.add_roles(role, reason=reason)


def setup(bot):
    bot.add_cog(GuestHandler(bot))
