from discord.ext import commands
import logging
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


def setup(bot):
    bot.add_cog(Events(bot))
