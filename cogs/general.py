from discord.ext import commands
from discord.ext.commands import has_permissions
from musicbot import utils
from musicbot.audiocontroller import AudioController
from musicbot.utils import guild_to_audiocontroller, guild_to_settings


class General(commands.Cog):
    """Commands for moving the bot around the server."""

    def __init__(self, stonks):
        self.stonks = stonks

    @commands.command(name='connect', help="Connect bot to voice channel.", aliases=["c"])
    async def _connect(self, ctx):  # dest_channel_name: str
        await self.uconnect(ctx)
    # logic is split to uconnect() for wide usage

    async def uconnect(self, ctx):

        vchannel = await utils.is_connected(ctx)

        if vchannel is not None:
            await ctx.send("Already connected to a voice channel.")
            return

        current_guild = utils.get_guild(self.stonks, ctx.message)

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return

        if utils.guild_to_audiocontroller[current_guild] is None:
            utils.guild_to_audiocontroller[current_guild] = AudioController(
                self.stonks, current_guild)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.stonks, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("Connected to {} {}".format(ctx.author.voice.channel.name, ":white_check_mark:"))

    @commands.command(name='disconnect', help="Disconnect bot from the voice channel.", aliases=["dc"])
    async def _disconnect(self, ctx, guild=False):
        await self.udisconnect(ctx, guild)

    async def udisconnect(self, ctx, guild):

        if guild is not False:

            current_guild = guild

            await utils.guild_to_audiocontroller[current_guild].stop_player()
            await current_guild.voice_client.disconnect(force=True)

        else:
            current_guild = utils.get_guild(self.stonks, ctx.message)

            if current_guild is None:
                await ctx.send("Please join a voice channel or enter the command in guild chat.")
                return

            if await utils.is_connected(ctx) is None:
                await ctx.send("Please join a voice channel or enter the command in guild chat.")
                return

            await utils.guild_to_audiocontroller[current_guild].stop_player()
            await current_guild.voice_client.disconnect(force=True)
            await ctx.send(f"Disconnected from voice channel. Use '{''}c' to rejoin.")

    @commands.command(name='reset',  help="Disconnect bot from the voice channel.", aliases=['rs'])
    async def _reset(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.stonks, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Connected to {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @commands.command(name='changechannel', help="Change the channel of the bot ", aliases=["cc"])
    async def _change_channel(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        vchannel = await utils.is_connected(ctx)
        if vchannel == ctx.author.voice.channel:
            await ctx.send("{} Already connected to {}".format(":white_check_mark:", vchannel.name))
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.stonks, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Switched to {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @commands.command(name='settings', help="View and set bot settings.")
    @has_permissions(administrator=True)
    async def _settings(self, ctx, *args):

        sett = guild_to_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed=await sett.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await sett.write(args[0], " ".join(args_list), ctx)

        if response is None:
            await ctx.send("`Error: Setting not found`")
        elif response is True:
            await ctx.send("Setting updated!")


def setup(stonks):
    stonks.add_cog(General(stonks))
