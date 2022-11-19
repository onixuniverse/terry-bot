from glob import glob

from nextcord.ext.commands import Bot
from nextcord.ext.commands.errors import ExtensionNotLoaded
from nextcord.flags import Intents
from loguru import logger

from utils.configs import get_prefix

COGS = [path.split('\\')[-1][:-3] for path in glob('cogs/*.py')]


class Terry(Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix(), intents=Intents.all(), help_command=None)

    def setup(self):
        logger.info('Loading cogs...')

        for cog in COGS:
            try:
                self.load_extension(f'cogs.{cog}')
                logger.info(f'{cog} loaded!')
            except ExtensionNotLoaded:
                logger.error(ExtensionNotLoaded)

    def run(self, bot_token):
        self.setup()
        super().run(bot_token, reconnect=True)

    async def on_ready(self):
        logger.info('Bot successfully started!')
