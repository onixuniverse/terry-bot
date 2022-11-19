from configparser import ConfigParser
from pathlib import Path

config_file_path = Path("resources/config.ini")


def append_to_config_file(config: ConfigParser):
    with open(config_file_path, "a") as config_file:
        config.write(config_file)


def write_default_config():
    if not config_file_path.exists():
        config = ConfigParser()
        config["DEFAULT"] = {"prefix": "/"}

        with open(config_file_path, "w") as config_file:
            config.write(config_file)


def write_config(guild_id, *args):
    config = ConfigParser()
    config[guild_id] = {
        "abuse_mode": args[0],
        "guest_mode": args[1],
        "log_mode": args[2],
        "log_channel_id": "",
        "guest_role_id": "",
        "table_spreadshhet_id": ""
    }

    append_to_config_file(config)


def rewrite_config(guild_id, setting, mode):
    config = ConfigParser()
    config.read(config_file_path)

    config[str(guild_id)][setting] = mode

    with open(config_file_path, "w") as config_file:
        config.write(config_file)


def read_all_config(guild_id):
    config = ConfigParser()
    config.read(config_file_path)

    try:
        result = config[str(guild_id)]
        return result
    except KeyError:
        return None


def read_config(guild_id, setting: str):
    config = ConfigParser()
    config.read(config_file_path)

    result = config[str(guild_id)][str(setting)]

    return result


def get_prefix():
    config = ConfigParser()
    config.read(config_file_path)

    prefix = config["DEFAULT"]["prefix"]

    return prefix

