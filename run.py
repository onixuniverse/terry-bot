import os

from dotenv import load_dotenv

from terry.main import Terry
from utils.configs import write_default_config, get_prefix

if __name__ == "__main__":
    load_dotenv()
    write_default_config()

    terry = Terry()
    terry.run(os.getenv("BOT_TOKEN"))

