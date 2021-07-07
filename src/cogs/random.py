import os
import praw
import random
from discord.ext import commands
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
        meme = reddit_memes(subreddit)
        await ctx.send(meme)

    @commands.command(help="")
    async def counter(self, ctx: commands.Context):
        """Starts a counter for pressing."""
        await ctx.send("Press!")


def setup(bot):
    bot.add_cog(Random(bot))


def reddit_memes(subreddit_id):
    reddit = praw.Reddit(
        client_id=user_id,
        client_secret=secret,
        user_agent="windows.com.bot.myredditbot:v1",
    )
    submission = reddit.subreddit(subreddit_id).top()
    top = random.randint(1, 25)
    random_sub = ""
    for i in range(top):
        random_sub = next(x for x in submission if not x.stickied)
    return random_sub.url
