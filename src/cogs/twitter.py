import os
import discord
import tweepy
import random
import asyncio
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime
from discord.ext.commands import command

load_dotenv()
api_key = os.environ.get("TWITTER_API")
secret = os.environ.get("TWITTER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_secret = os.environ.get("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuthHandler(api_key, secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class Twitter(commands.Cog):
    def __init__(self, stonks):
        self.stonks = stonks
        # self.twitter_task.start()
        self.latest = []
        self.channels = None

    def cog_unload(self):
        self.twitter_task.cancel()

    @tasks.loop(minutes=5)
    async def twitter_task(self):
        timeline = api.home_timeline(count=1, tweet_mode="extended")
        channel = self.stonks.get_channel(794886689654177792)
        for tweet in timeline:
            try:
                if tweet.full_text == self.latest:
                    break
                else:
                    y = datetime.now()
                    x = y.strftime("%H:%M:%S, %d/%m/%Y")
                    self.latest = tweet.full_text
                    await channel.send(
                        f"Tweet from: {tweet.user.name}\nTweet created at: {x}\n{tweet.full_text}"
                    )
            except AttributeError:
                continue

    @tasks.loop(minutes=5)
    async def twitter_user_task(self):
        data = cr.execute(f"SELECT channel_id FROM twitter").fetchone()[0]
        self.channels = data
        timeline = api.user_timeline(count=1, tweet_mode="extended")
        for tweet in timeline:
            try:
                if tweet.full_text == self.latest:
                    break
                else:
                    y = datetime.now()
                    x = y.strftime("%H:%M:%S, %d/%m/%Y")
                    self.latest = tweet.full_text
                    # await channel.send(f"Tweet from: {tweet.user.name}\nTweet created at: {x}\n{tweet.full_text}")
            except AttributeError:
                continue

    @command(help="Subscribe to twitter feed, add ONE channel what to follow.")
    @commands.has_permissions(administrator=True)
    async def twitter_join(self, ctx, *, message):
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        try:
            if cr.execute(
                f"SELECT channel1 FROM twitter WHERE guild_id = {guild_id} AND channel_id = {channel_id}"
            ).fetchone()[0]:
                await ctx.channel.send(
                    f"Channel is already subscribed to twitter feed! Use 'twitter_add to add more users!'"
                )
        except TypeError:
            cr.execute(
                "INSERT OR IGNORE INTO twitter(guild_id, channel_id, channel1) VALUES (?, ?, ?)",
                (guild_id, channel_id, message),
            )
            commit()
            await ctx.channel.send(
                f"Successfully subscribed twitter feed and added {message} to it!"
            )

    @command(help="Add users to your feed.")
    @commands.has_permissions(administrator=True)
    async def twitter_add(self, ctx, *, message):
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        cr.execute(
            "INSERT OR IGNORE INTO twitter(guild_id, channel_id, channel1) VALUES (?, ?, ?)",
            (guild_id, channel_id, message),
        )
        commit()
        await ctx.channel.send(f"User {message} successfully added to twitter feed!")


def setup(stonks):
    stonks.add_cog(Twitter(stonks))


# data = cr.execute(f"SELECT channel1 FROM twitter WHERE channel_id={823569976002347060}").fetchall()
# for i in data:
#     print(i[0])


def twitter_timeline():
    timelines = ["JukkaLepikko", "mikko"]
    timeline = api.user_timeline(
        screen_name="JukkaLepikko", count=1, tweet_mode="extended", exclude_replies=True
    )
    for tweet in timeline:
        print(tweet.full_text)
