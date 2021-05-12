import discord
import asyncio
from discord.ext import commands
from musicbot import utils
from musicbot import linkutils
from cogs.general import General


class Music(commands.Cog):
    """ Plays music from youtube or spotify."""

    def __init__(self, stonks):
        self.stonks = stonks

    @commands.command(name='play', help="Play a supported link or search from youtube.", aliases=['p'])
    async def _play_song(self, ctx, *, track: str):

        if await utils.is_connected(ctx) is None:
            await General.uconnect(self, ctx)
        if track.isspace() or not track:
            return

        if await utils.play_check(ctx) is False:
            return

        current_guild = utils.get_guild(self.stonks, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if audiocontroller.playlist.loop == True:
            await ctx.send(f"Loop is enabled! Use {''} loop to disable.")
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send("Unknown site :question:")
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song is not None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output("Now Playing."))
            else:
                await ctx.send(embed=song.info.format_output("Added to queue."))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send("Queued playlist :page_with_curl:")

    @commands.command(name='loop', help="Loops the currently playing song, toggle on/off.", aliases=['l'])
    async def _loop(self, ctx):

        current_guild = utils.get_guild(self.stonks, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) is False:
            return

        if len(audiocontroller.playlist.playque) < 1:
            await ctx.send("No songs in queue!")
            return

        if audiocontroller.playlist.loop is False:
            audiocontroller.playlist.loop = True
            await ctx.send("Loop enabled :arrows_counterclockwise:")
        else:
            audiocontroller.playlist.loop = False
            await ctx.send("Loop disabled :x:")

    @commands.command(name='shuffle', help="Shuffle the queue.", aliases=["sh"])
    async def _shuffle(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) is False:
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Queue is empty :x:")
            return

        audiocontroller.playlist.shuffle()
        await ctx.send("Shuffled queue :twisted_rightwards_arrows:")

        for song in list(audiocontroller.playlist.playque)[:5]:
            asyncio.ensure_future(audiocontroller.preload(song))

    @commands.command(name='pause', help="Pause the song.")
    async def _pause(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await ctx.send("Playback Paused :pause_button:")

    @commands.command(name='queue', help="Shows the songs in queue.", aliases=["playlist", "plist"])
    async def _queue(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Queue is empty :x:")
            return

        playlist = utils.guild_to_audiocontroller[current_guild].playlist

        embed = discord.Embed(title=":scroll: Queue [{}]".format(
            len(playlist.playque)), color=discord.Color.random(), inline=False)

        counter = 1
        for song in list(playlist.playque)[:5]:
            if song.info.title is None:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.webpage_url, song.info.webpage_url), inline=False)
            else:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.title, song.info.webpage_url), inline=False)
            counter = counter + 1

        await ctx.send(embed=embed)

    @commands.command(name='stop', help="Stop the song.")
    async def _stop(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await ctx.send("Stopped all sessions :octagonal_sign:")

    @commands.command(name='skip', help="Skip a song.", aliases=["s"])
    async def _skip(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            return
        current_guild.voice_client.stop()
        await ctx.send("Skipped current song :fast_forward:")

    @commands.command(name='clear', help="Clear the queue.", aliases=["cl"])
    async def _clear(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        await ctx.send("Cleared queue :no_entry_sign:")

    @commands.command(name='prev', help="Go back one song.")
    async def _prev(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        await utils.guild_to_audiocontroller[current_guild].prev_song()
        await ctx.send("Playing previous song :track_previous:")

    @commands.command(name='resume', help="Resume song.")
    async def _resume(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        current_guild.voice_client.resume()
        await ctx.send("Resumed playback :arrow_forward:")

    @commands.command(name='songinfo',  help="Info about current song.", aliases=["sinfo"])
    async def _songinfo(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.send(embed=song.info.format_output("Song info."))

    @commands.command(name='history', aliases=["hist"], help="Show history of songs.")
    async def _history(self, ctx):
        current_guild = utils.get_guild(self.stonks, ctx.message)

        if await utils.play_check(ctx) is False:
            return

        if current_guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return
        await ctx.send(utils.guild_to_audiocontroller[current_guild].track_history())

    @commands.command(name='volume', aliases=["vol"], help="Change the volume.")
    async def _volume(self, ctx, *args):
        if ctx.guild is None:
            await ctx.send("Please join a voice channel or enter the command in guild chat.")
            return

        if await utils.play_check(ctx) is False:
            return

        if len(args) == 0:
            await ctx.send("Current volume: {}% :speaker:".format(utils.guild_to_audiocontroller[ctx.guild]._volume))
            return

        try:
            volume = args[0]
            volume = int(volume)
            if volume > 100:
                raise Exception('')
            current_guild = utils.get_guild(self.stonks, ctx.message)

            if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
                await ctx.send('Volume set to {}% :sound:'.format(str(volume)))
            else:
                await ctx.send('Volume set to {}% :loud_sound:'.format(str(volume)))
            utils.guild_to_audiocontroller[current_guild].volume = volume
        except:
            await ctx.send("Error: Volume must be a number 1-100")


def setup(stonks):
    stonks.add_cog(Music(stonks))
