import asyncio
import logging
import math
import discord
import youtube_dl
from discord.ext import commands
from musicbot import config
from musicbot import video as vid


FFMPEG_BEFORE_OPTS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"


async def audio_playing(ctx):
    """Checks that audio is currently playing before continuing."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        raise commands.CommandError("Not currently playing any audio.")


async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if (
        voice
        and bot_voice
        and voice.channel
        and bot_voice.channel
        and voice.channel == bot_voice.channel
    ):
        return True
    else:
        raise commands.CommandError("You need to be in the channel to do that.")


async def is_audio_requester(ctx):
    """Checks that the command sender is the song requester."""
    music = ctx.stonks.get_cog("Music")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        raise commands.CommandError("You need to be the song requester to do that.")


class Music(commands.Cog):
    """Bot commands to help play music."""

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config[__name__.split(".")[-1]]
        self.states = {}
        self.bot.add_listener(self.on_reaction_add, "on_reaction_add")

    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @commands.command(aliases=["stop"], help="Bot leaves voice channel.")
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Not in a voice channel.")

    @commands.command(
        aliases=["resume", "p"], help="Pause any currently playing audio."
    )
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    @commands.check(is_audio_requester)
    async def pause(self, ctx):
        client = ctx.guild.voice_client
        self._pause_audio(client)

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    @commands.command(aliases=["vol", "v"], help="Change current volume (values 0-250)")
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    @commands.check(is_audio_requester)
    async def volume(self, ctx, volume: int):
        state = self.get_state(ctx.guild)

        if volume < 0:
            volume = 0

        max_vol = self.config["max_volume"]
        if -1 < max_vol < volume:
            volume = max_vol

        client = ctx.guild.voice_client

        state.volume = float(volume) / 100.0
        client.source.volume = state.volume

    @commands.command(help="Skip current song.")
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx):
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(
            ctx.author
        ):

            client.stop()
        elif self.config["vote_skip"]:

            channel = client.channel
            self._vote_skip(channel, ctx.author)

            users_in_channel = len(
                [member for member in channel.members if not member.bot]
            )
            required_votes = math.ceil(
                self.config["vote_skip_ratio"] * users_in_channel
            )
            await ctx.send(
                f"{ctx.author.mention} voted to skip ({len(state.skip_votes)}/{required_votes} votes)"
            )
        else:
            raise commands.CommandError("Sorry, vote skipping is disabled.")

    def _vote_skip(self, channel, member):
        """Register a vote for `member` to skip the song playing."""
        logging.info(f"{member.name} votes to skip")
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([member for member in channel.members if not member.bot])
        if (float(len(state.skip_votes)) / users_in_channel) >= self.config[
            "vote_skip_ratio"
        ]:

            logging.info(f"Enough votes, skipping...")
            channel.guild.voice_client.stop()

    def _play_song(self, client, state, song):
        state.now_playing = song
        state.skip_votes = set()
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, before_options=FFMPEG_BEFORE_OPTS),
            volume=state.volume,
        )

        def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)

        client.play(source, after=after_playing)

    @commands.command(aliases=["np"], help="Display information about current song.")
    @commands.check(audio_playing)
    async def nowplaying(self, ctx):
        state = self.get_state(ctx.guild)
        message = await ctx.send("", embed=state.now_playing.get_embed())
        await self._add_reaction_controls(message)

    @commands.command(aliases=["q", "playlist"], help="Display current play queue.")
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        state = self.get_state(ctx.guild)
        await ctx.send(self._queue_text(state.playlist))

    def _queue_text(self, queue):
        if len(queue) > 0:
            message = [f"{len(queue)} songs in queue:"]
            message += [
                f"  {index+1}. **{song.title}** (requested by **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]
            return "\n".join(message)
        else:
            return "The play queue is empty."

    @commands.command(aliases=["cl"], help="Clear the play queue.")
    @commands.check(audio_playing)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        state = self.get_state(ctx.guild)
        state.playlist = []

    @commands.command(aliases=["jq"], help="Jump to song <index>")
    @commands.check(audio_playing)
    @commands.has_permissions(administrator=True)
    async def jump(self, ctx, song: int, new_index: int):
        state = self.get_state(ctx.guild)
        if 1 <= song <= len(state.playlist) and 1 <= new_index:
            song = state.playlist.pop(song - 1)
            state.playlist.insert(new_index - 1, song)

            await ctx.send(self._queue_text(state.playlist))
        else:
            raise commands.CommandError("You must use a valid index.")

    @commands.command(help="Plays audio from <url>.")
    async def play(self, ctx, *, url):
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)

        if client and client.channel:
            try:
                video = vid.Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                logging.warning(f"Error downloading video: {e}")
                await ctx.send("There was an error downloading your video, sorry.")
                return
            state.playlist.append(video)
            message = await ctx.send("Added to queue.", embed=video.get_embed())
            await self._add_reaction_controls(message)
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    video = vid.Video(url, ctx.author)
                except youtube_dl.DownloadError as e:
                    await ctx.send("There was an error downloading your video, sorry.")
                    return
                client = await channel.connect()
                self._play_song(client, state, video)
                message = await ctx.send("", embed=video.get_embed())
                await self._add_reaction_controls(message)
                logging.info(f"Now playing '{video.title}'")
            else:
                raise commands.CommandError(
                    "You need to be in a voice channel to do that."
                )

    async def on_reaction_add(self, reaction, user):
        """Responds to reactions added to the stonk's messages, allowing reactions to control playback."""
        message = reaction.message
        if user != self.bot.user and message.author == self.bot.user:
            await message.remove_reaction(reaction, user)
            if message.guild and message.guild.voice_client:
                user_in_channel = (
                    user.voice
                    and user.voice.channel
                    and user.voice.channel == message.guild.voice_client.channel
                )
                permissions = message.channel.permissions_for(user)
                guild = message.guild
                state = self.get_state(guild)
                if permissions.administrator or (
                    user_in_channel and state.is_requester(user)
                ):
                    client = message.guild.voice_client
                    if reaction.emoji == "⏯":
                        self._pause_audio(client)
                    elif reaction.emoji == "⏭":
                        client.stop()
                    elif reaction.emoji == "⏮":
                        state.playlist.insert(0, state.now_playing)
                        client.stop()
                elif (
                    reaction.emoji == "⏭"
                    and self.config["vote_skip"]
                    and user_in_channel
                    and message.guild.voice_client
                    and message.guild.voice_client.channel
                ):
                    voice_channel = message.guild.voice_client.channel
                    self._vote_skip(voice_channel, user)

                    channel = message.channel
                    users_in_channel = len(
                        [member for member in voice_channel.members if not member.bot]
                    )
                    required_votes = math.ceil(
                        self.config["vote_skip_ratio"] * users_in_channel
                    )
                    await channel.send(
                        f"{user.mention} voted to skip ({len(state.skip_votes)}/{required_votes} votes)"
                    )

    async def _add_reaction_controls(self, message):
        """Adds a 'control-panel' of reactions to a message that can be used to control the bot."""
        controls = ["⏮", "⏯", "⏭"]
        for control in controls:
            await message.add_reaction(control)


def setup(bot):
    cfg = config.load_config()
    bot.add_cog(Music(bot, cfg))


class GuildState:
    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.skip_votes = set()
        self.now_playing = None

    def is_requester(self, user):
        return self.now_playing.requested_by == user
