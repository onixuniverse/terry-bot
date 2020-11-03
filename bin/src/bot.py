from glob import glob

from resources.data.config import OWNER_IDS, PREFIX
from discord.ext.commands import Bot
from discord.ext.commands.errors import ExtensionNotLoaded
from discord.flags import Intents
from loguru import logger

COGS = [path.split('\\')[-1][:-3] for path in glob('bin/cogs/*.py')]


@logger.catch
class Bot(Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        
        super().__init__(command_prefix=PREFIX, OWNER_IDS=OWNER_IDS, intents=Intents.all())
        
    def setup(self):
        for cog in COGS:
            try:
                self.load_extension(f'bin.cogs.{cog}')
                logger.info(f'{cog} loaded')
            except ExtensionNotLoaded as exc:
                logger.error(exc)
    
    def run(self, version):
        self.VERSION = version

        logger.info('Setuping cogs...')
        self.setup()
        
        with open('resources\\data\\tokens\\token', 'r') as tf:
            self.TOKEN = tf.read()
            
        logger.info('Starting bot...')
        super().run(self.TOKEN, reconnect=True)

    
    async def on_ready(self):
        logger.info('Bot ready!')


bot = Bot()
