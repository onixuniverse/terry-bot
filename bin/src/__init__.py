from glob import glob
from loguru import logger
from discord.ext.commands import Bot
from discord.flags import Intents

from data.config import PREFIX, OWNER_IDS


COGS = [path.split('\\')[-1][:-3] for path in glob('./bin/cogs/*.py')]
INTENTS = Intents.all()


@logger.catch
class Bot(Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        self.INTENTS = INTENTS
        
        super().__init__(command_prefix=PREFIX, OWNER_IDS=OWNER_IDS, intents=INTENTS)
        
    def setup(self):
        for cog in COGS:
            self.load_extension(f'bin.cogs.{cog}')
            logger.info(f'{cog} loaded')
    
    def run(self, version):
        self.VERSION = version

        logger.info('Setuping cogs...')
        self.setup()
        
        with open('data/token', 'r') as tf:
            self.TOKEN = tf.read()
            
        logger.info('Starting bot...')
        super().run(self.TOKEN, reconnect=True)

    
    async def on_ready(self):
        logger.info('Bot ready!')


bot = Bot()
