import os
import sys
from cogs import utils
from discord.ext import commands
from dotenv import load_dotenv
from utility import setup


load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = os.environ.get("GUILD")
OWNER = os.environ.get("OWNER")

if __name__ == "__main__":

    current_directory = os.path.dirname(os.path.abspath(__file__))

    bot = commands.Bot(
        command_prefix=setup.get_prefix,
        description="Hackerman",
        intents=setup.bot_intents(),
        owner_id=int(OWNER),
        case_insensitive=True,
    )
    bot.cog_list = [
        "cogs.default",
        "cogs.errors",
        "cogs.mod",
        "cogs.music",
        "cogs.random",
        "cogs.utils",
        "cogs.finance",
        "cogs.core.events",
    ]
    logger = setup.setup_logging()
    bot.logger = logger

    if TOKEN == "":
        print("Error: No bot token!")

    for cog in bot.cog_list:
        logger.info(f"Loading extension: {cog}")
        bot.load_extension(cog)
    bot.help_command = utils.MyHelp()
    # bot.help_command = utils.MyNewHelp()


bot.run(TOKEN)
