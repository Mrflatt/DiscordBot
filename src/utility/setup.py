import logging
import os
from discord import Intents
import json

current_directory = os.path.dirname(os.path.abspath(__file__))


def get_prefix(ctx, message):
    with open(f"{current_directory}/prefixes.json", "r") as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]


def set_prefix(guild, prefix="$"):
    with open(f"{current_directory}/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = prefix
    with open(f"{current_directory}/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


def remove_prefix(guild):
    with open(f"{current_directory}/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open(f"{current_directory}/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


def setup_logging() -> logging.Logger:
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def bot_intents() -> Intents:
    intents = Intents.all()
    intents.guilds = True
    intents.members = True
    intents.bans = True
    intents.emojis = True
    intents.integrations = True
    intents.webhooks = True
    intents.invites = True
    intents.voice_states = True
    intents.presences = True
    intents.messages = True
    intents.guild_messages = True
    intents.dm_messages = True
    intents.reactions = True
    intents.guild_reactions = True
    intents.dm_reactions = True
    intents.typing = True
    intents.guild_typing = True
    intents.dm_typing = True

    return intents
