import json
import os
import discord
import logging
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp

load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = os.environ.get("GUILD")
OWNER = os.environ.get("OWNER")
intents = Intents.all()


def get_prefix(client, message):
    with open(f"{current_directory}/prefixes.json", "r") as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]


stonks = commands.Bot(
    command_prefix=get_prefix,
    description="Hackerman",
    intents=intents,
    owner_id=int(OWNER),
    case_insensitive=True,
)


stonks.help_command = PrettyHelp()

if __name__ == "__main__":

    current_directory = os.path.dirname(os.path.abspath(__file__))
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if TOKEN == "":
        print("Error: No bot token!")

    for cog in os.listdir(f"{current_directory}/cogs"):
        if cog.endswith(".py") and cog != "__init__.py":
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                stonks.load_extension(cog)
            except Exception as e:
                print(f"{cog} can not be loaded")
                raise e


class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return "%s%s %s" % (
            self.clean_prefix,
            command.qualified_name,
            command.signature,
        )

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.random())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(
                    name=cog_name, value="\n".join(command_signatures), inline=False
                )

        channel = self.get_destination()
        await channel.send(embed=embed)


class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emb = discord.Embed(description=page)
            await destination.send(embed=emb)


stonks.help_command = MyNewHelp()


@stonks.event
async def on_ready():
    print(f"{stonks.user.name} is ready!")
    await stonks.change_presence(activity=discord.Game("discord API"))
    print("Startup done!")


@stonks.event
async def on_guild_join(guild):
    with open(f"{current_directory}/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "$"
    with open(f"{current_directory}/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@stonks.event
async def on_guild_remove(guild):
    with open(f"{current_directory}/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open(f"{current_directory}/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@stonks.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    stonks.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} loaded!", delete_after=20)


@stonks.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    stonks.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} unloaded!", delete_after=20)


@stonks.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    stonks.unload_extension(f"cogs.{extension}")
    stonks.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} reloaded!", delete_after=20)


stonks.run(TOKEN)
