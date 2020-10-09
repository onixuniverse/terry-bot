from discord.ext.commands import Bot


PREFIX = '!'
OWNER_IDS = [233628188968747008]


bot = Bot(command_prefix=PREFIX, help_command=None, owner_ids=OWNER_IDS)

async def on_connect():
    print('Bot connected')


async def on_disconnect():
    print('Bot disconected')
    
    
async def on_ready():
    pass


bot.run('NzY0MTA3MTY1MTEwNjMyNDQ4.X4BcQA.cIOqEWD42z4RnNaaW8yt6pEQiio')