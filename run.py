import os

from terry.bin.src.terry import bot
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")


# Run bot
bot.run(bot_token)
