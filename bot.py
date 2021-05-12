import os
import discord
import logging
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp, Navigation
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from config import config
from musicbot.utils import guild_to_audiocontroller, guild_to_settings
from cogs.general import General
load_dotenv()
TOKEN = os.environ.get('TOKEN')
GUILD = os.environ.get('GUILD')
intents = Intents.all()
stonks_auto_join = False

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


stonks = commands.Bot(command_prefix="-", description="Hackerman", intents=intents, owner_id=os.environ.get('OWNER'), case_insensitive=True)

nav = Navigation(":discord:743511195197374563", "\:arrow_left:", "\:arrow_right")
stonks.help_command = PrettyHelp()

if __name__ == '__main__':

    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if TOKEN == "":
        print("Error: No bot token!")

    for cog in os.listdir(".\cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                stonks.load_extension(cog)
            except Exception as e:
                print(f"{cog} can not be loaded")
                raise e


class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.random())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emb = discord.Embed(description=page)
            await destination.send(embed=emb)


# stonks.help_command = MyHelp()

@stonks.event
async def on_ready():
    print(f"{stonks.user.name} is ready!")
    for guild in stonks.guilds:
        await register(guild)
    print("Startup done!")


@stonks.event  # When bots joins a server, default prefix is ".", saves it to json
async def on_guild_join(guild):
    await register(guild)


@stonks.event  # When bots leaves a server, default prefix is removed from json
async def on_guild_remove(guild):
    await register(guild)


@stonks.command(hidden=True)  # Loads on extension
@commands.is_owner()
async def load(ctx, extension):
    stonks.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} loaded!", delete_after=20)


@stonks.command(hidden=True)  # Unloads on extension
@commands.is_owner()
async def unload(ctx, extension):
    stonks.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} unloaded!", delete_after=20)


@stonks.command(hidden=True)  # Reloads on extension
@commands.is_owner()
async def reload(ctx, extension):
    stonks.unload_extension(f"cogs.{extension}")
    stonks.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} reloaded!", delete_after=20)


async def register(guild):

    guild_to_settings[guild] = Settings(guild)
    guild_to_audiocontroller[guild] = AudioController(stonks, guild)
    vc_channels = guild.voice_channels
    if stonks_auto_join:
        start_vc = guild_to_settings[guild].get('start_voice_channel')
        if start_vc is not None:
            for vc in vc_channels:
                if vc.id == start_vc:
                    await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    await General.udisconnect(self=None, ctx=None, guild=guild)
                    try:
                        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    except Exception as e:
                        print(e)
        else:
            await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            await General.udisconnect(self=None, ctx=None, guild=guild)
            try:
                await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            except Exception as e:
                print(e)


stonks.run(TOKEN)
