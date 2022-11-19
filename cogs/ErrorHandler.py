from nextcord.errors import Forbidden, HTTPException
from nextcord.ext.commands import Cog
from nextcord.ext.commands.errors import (BadArgument, BotMissingPermissions, CommandNotFound, CommandOnCooldown,
                                          DisabledCommand, MemberNotFound, MissingPermissions, MissingRequiredArgument,
                                          NSFWChannelRequired, RoleNotFound)
from loguru import logger

IGNORE_EXCEPTIONS = [BadArgument, CommandNotFound, DisabledCommand]


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, exc):
        """Вывод некоторых исключений"""
        if any(isinstance(exc, err) for err in IGNORE_EXCEPTIONS):
            pass
        elif isinstance(exc, MissingPermissions):
            await ctx.send('У тебя нет прав!')
        elif isinstance(exc, BotMissingPermissions):
            await ctx.send('У меня нет прав!')
        elif isinstance(exc, NSFWChannelRequired):
            await ctx.send(f'У канала `{exc.channel}` нет статуса NSFW!')
        elif isinstance(exc, MemberNotFound):
            await ctx.send(f'Пользователь не найден. `{exc.argument}`')
        elif isinstance(exc, RoleNotFound):
            await ctx.send(f'Роль не найдена. `{exc.argument}`')
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send('Задержка команды. Попробуй через: {exc.retry_after:.2f}сек.')
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(f'Пропущен требуемый аргумент: `{exc.param}`')
        elif isinstance(exc, DisabledCommand):
            await ctx.send('Команда временно отключена.')
        elif isinstance(exc.original, HTTPException):
            logger.error(HTTPException)
        elif isinstance(exc.original, Forbidden):
            logger.error(Forbidden)
        else:
            logger.error(exc)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
