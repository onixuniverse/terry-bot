from glob import glob

from discord.ext.commands import Bot
from discord.ext.commands.errors import ExtensionNotLoaded
from discord.flags import Intents
from loguru import logger

from terry.resources.data.config import OWNER_IDS, PREFIX

COGS = [path.split('\\')[-1][:-3] for path in glob('terry/bin/cogs/*.py')]


class Bot(Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        super().__init__(command_prefix=PREFIX, OWNER_IDS=OWNER_IDS, intents=Intents.all(), help_command=None)

    def setup(self):
        logger.info('Setting cogs...')

        for cog in COGS:
            try:
                self.load_extension(f'bin.cogs.{cog}')
                logger.info(f'{cog} setup!')
            except ExtensionNotLoaded:
                logger.error(ExtensionNotLoaded)

    def run(self, version):
        self.VERSION = version

        with open('terry/resources/data/tokens/token', 'r') as tf:
            self.TOKEN = tf.read()

        self.setup()
        super().run(self.TOKEN, reconnect=True)

    async def on_ready(self):
        logger.info('Bot started!')


_bot = Bot()
