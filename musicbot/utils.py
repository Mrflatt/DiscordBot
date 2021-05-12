# A dictionary that remembers which guild belongs to which audiocontroller
guild_to_audiocontroller = {}

# A dictionary that remembers which settings belongs to which guild
guild_to_settings = {}


def get_guild(stonks, command):
    """Gets the guild a command belongs to. Useful, if the command was sent via pm."""
    if command.guild is not None:
        return command.guild
    for guild in stonks.guilds:
        for channel in guild.voice_channels:
            if command.author in channel.members:
                return guild
    return None


async def connect_to_channel(guild, dest_channel_name, ctx, switch=False, default=True):
    """Connects the bot to the specified voice channel."""
    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(dest_channel_name).strip():
            if switch:
                try:
                    await guild.voice_client.disconnect()
                except:
                    await ctx.send("Bot not connected to any voice channel.")

            await channel.connect()
            return

    if default:
        try:
            await guild.voice_channels[0].connect()
        except:
            await ctx.send("Could not join the default voice channel.")
    else:
        await ctx.send("Could not find channel." + str(dest_channel_name))


async def is_connected(ctx):
    try:
        voice_channel = ctx.guild.voice_client.channel
        return voice_channel
    except:
        return None


async def play_check(ctx):
    sett = guild_to_settings[ctx.guild]
    cm_channel = sett.get('command_channel')
    vc_rule = sett.get('user_must_be_in_vc')

    if cm_channel is not None:
        if cm_channel != ctx.message.channel.id:
            await ctx.send("Please use configured command channel.")
            return False

    if vc_rule:
        author_voice = ctx.message.author.voice
        bot_vc = ctx.guild.voice_client.channel
        if author_voice is None:
            await ctx.send("Please join the voice channel to use commands.")
            return False
        elif ctx.message.author.voice.channel != bot_vc:
            await ctx.send("Please join the voice channel to use commands.")
            return False
