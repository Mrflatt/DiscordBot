from discord.ext import commands
import discord
import asyncio
from utility import setup


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"{self.bot.user.name} is ready!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        setup.set_prefix(guild.id)
        await asyncio.sleep(2)

        for channel in guild.text_channels:
            if "general" in channel.name:
                embed = discord.Embed(
                    color=self.d.cc,
                    description=f"Hey y'all! Type `$help` to get started with Bot!\n"
                    f"If you need any more help, check out the **[Github](https://github.com/Mrflatt/DiscordBot)**!",
                )
                embed.set_author(name="Bot")
                embed.set_footer(text=f"Made by MrFlatt!")

                await channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        setup.remove_prefix(guild.id)

    @commands.Cog.listener()  # When user joins a server message
    async def on_member_join(self, member):
        channel = self.bot.get_channel(794886689654177792)
        if not channel:
            return
        await channel.send(
            f"Welcome! {member.mention} Play safe! You are {len(list(member.guild.members))} member."
        )

    @commands.Cog.listener()  # Listen to this messages on chat
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "homo" in message.content.lower():
            await message.channel.send("No ei kai siinä")
        if "lauri" in message.content.lower():
            await message.channel.send("Kuka niistä?")
        if "fortnite" in message.content.lower():
            await message.channel.purge(limit=1)


def setup(bot):
    bot.add_cog(Events(bot))
