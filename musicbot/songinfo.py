import discord
import datetime
from discord.ext import commands


class Song:
    def __init__(self, origin, host, base_url=None, uploader=None, title=None, duration=None, webpage_url=None, thumbnail=None):
        self.host = host
        self.origin = origin
        self.base_url = base_url
        self.info = self.Sinfo(uploader, title, duration,
                               webpage_url, thumbnail)

    class Sinfo:
        def __init__(self, uploader, title, duration, webpage_url, thumbnail):
            self.uploader = uploader
            self.title = title
            self.duration = duration
            self.webpage_url = webpage_url
            self.thumbnail = thumbnail
            self.output = ""

        def format_output(self, playtype):

            embed = discord.Embed(title=playtype, description="[{}]({})".format(self.title, self.webpage_url), color=discord.Color.random())

            if self.thumbnail is not None:
                embed.set_thumbnail(url=self.thumbnail)

            embed.add_field(name="Uploader: ",
                            value=self.uploader, inline=False)

            if self.duration is not None:
                embed.add_field(name="Duration: ",
                                value="{}".format(str(datetime.timedelta(seconds=self.duration))), inline=False)
            else:
                embed.add_field(name="Duration: ",
                                value="Unknown", inline=False)

            return embed