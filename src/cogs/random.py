import os
import discord
from discord.ext import commands
from utility import helpers
from dotenv import load_dotenv

load_dotenv()
user_id = os.environ.get("REDDIT_ID")
secret = os.environ.get("REDDIT_SECRET")
password = os.environ.get("REDDIT_PASSWORD")


class Random(commands.Cog):
    """Posts from different social platforms"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Random post from reddit, default 'memes'")
    async def meme(self, ctx, *, subreddit="memes"):
        meme = helpers.reddit_memes(subreddit)
        await ctx.send(meme)

    @commands.command(help="")
    async def counter(ctx: commands.Context):
        """Starts a counter for pressing."""
        await ctx.send("Press!")


def setup(bot):
    bot.add_cog(Random(bot))
