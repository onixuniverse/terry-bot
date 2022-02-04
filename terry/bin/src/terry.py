from glob import glob

from discord.ext.commands import Bot
from discord.ext.commands.errors import ExtensionNotLoaded
from discord.flags import Intents
from loguru import logger

from terry.resources.data.config import OWNER_IDS, PREFIX

COGS = [path.split('\\')[-1][:-3] for path in glob('terry/bin/cogs/*.py')]


class Terry(Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        super().__init__(command_prefix=PREFIX, OWNER_IDS=OWNER_IDS, intents=Intents.all(), help_command=None)

    def setup(self):
        logger.info('Loading cogs...')

        for cog in COGS:
            try:
                self.load_extension(f'terry.bin.cogs.{cog}')
                logger.info(f'{cog} loaded!')
            except ExtensionNotLoaded:
                logger.error(ExtensionNotLoaded)

    def run(self, bot_token):
        self.setup()
        super().run(bot_token, reconnect=True)

    async def on_ready(self):
        logger.info('Bot successfully started!')


bot = Terry()
