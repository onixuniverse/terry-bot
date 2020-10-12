from glob import glob
from discord.ext.commands import Bot

from bin.bot.config import PREFIX, OWNER_IDS


COGS = [path.split('\\')[-1][:-3] for path in glob('./bin/cogs/*.py')]

class Bot(Bot):
    def __init__(self):
        self.PREFIX = PREFIX
        
        super().__init__(command_prefix=PREFIX, OWNER_IDS=OWNER_IDS)
        
    def setup(self):
        for cog in COGS:
            self.load_extension(f'bin.cogs.{cog}')
            print(f'{cog} loaded')
    
    def run(self, version):
        self.VERSION = version
        
        print('Setuping cogs...')
        self.setup()
        
        with open('data/token', 'r') as tf:
            self.TOKEN = tf.read()
            
        print('Starting bot...')
        super().run(self.TOKEN, reconnect=True)

    
    async def on_ready(self):
        print('Bot ready!')

bot = Bot()
