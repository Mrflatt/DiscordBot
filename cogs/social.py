import asyncpraw
import praw
import os
import discord
from discord.ext import commands
from utility import helpers
import random
from random import choice
from dotenv import load_dotenv

load_dotenv()
user_id = os.environ.get('REDDIT_ID')
secret = os.environ.get('REDDIT_SECRET')
password = os.environ.get('REDDIT_PASSWORD')


class Social(commands.Cog):
    """Posts from different social platforms"""
    def __init__(self, stonks):
        self.stonks = stonks

    @commands.command(help="Random post from reddit, default 'memes'")
    async def meme(self, ctx, *, subreddit='memes'):
        meme = helpers.reddit_memes(subreddit)
        await ctx.send(meme)


def setup(stonks):
    stonks.add_cog(Social(stonks))


"""async def reddit_sub():
    reddit = asyncpraw.Reddit(client_id=user_id, client_secret=secret, username="mauriitsio", password=password,
                              user_agent='windows.com.bot.myredditbot:v1')
    submission = await reddit.subreddit('Python').top()
    # async for submission in subreddit.stream.submissions():
    top = random.randint(1, 25)
    for i in range(top):
        random_sub = next(x for x in submission if not x.stickied)
        # random_sub = random.choice(list_subs)
        # name = random_sub.title
        em = discord.Embed(title=submission.name, color=discord.Color.gold())
        em.set_image(url=submission.url)
        return await random_sub.url"""



