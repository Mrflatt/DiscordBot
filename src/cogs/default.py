import asyncio
import os
from src.utility import helpers
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")


class Default(commands.Cog):
    """Different bot events, no commands."""

    def __init__(self, stonks):
        self.stonks = stonks
        self.stonks.loop.create_task(self.once_a_hour())

    @commands.Cog.listener()  # Prints reddit post and bitcoins value every even hour
    async def once_a_hour(self):
        await self.stonks.wait_until_ready()
        channel = self.stonks.get_channel(794886689654177792)
        while not self.stonks.is_closed():
            now_ = datetime.now().minute
            if now_ == 00:
                await channel.send(
                    f"Jos bitcoin droppaa alle 45k, niin pakko ostaa {helpers.bitcoin()}"
                )
                await channel.send(helpers.reddit_memes("wallstreetbets"))
                time_ = 90
            else:
                time_ = 10
            await asyncio.sleep(time_)

    @commands.Cog.listener()  # When user joins a server message
    async def on_member_join(self, member):
        channel = self.stonks.get_channel(794886689654177792)
        if not channel:
            return
        await channel.send(
            f"Welcome! {member.mention} Play safe! You are {len(list(member.guild.members))} member."
        )

    @commands.Cog.listener()  # Listen to this messages on chat
    async def on_message(self, message):
        if message.author == self.stonks.user:
            return
        if "homo" in message.content.lower():
            await message.channel.send("No ei kai siinä")
        if "lauri" in message.content.lower():
            await message.channel.send("Kuka niistä?")
        if "fortnite" in message.content.lower():
            await message.channel.purge(limit=1)


def setup(stonks):
    stonks.add_cog(Default(stonks))