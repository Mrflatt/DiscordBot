import os

import discord
import requests
import json
import time
from discord.ext import commands
from src.utility import helpers
from discord.ext.commands import command
from datetime import datetime
import aiohttp
import yfinance as yf

yf.pdr_override()


class Utils(commands.Cog):
    """Some useful commands, such as server and user info"""

    def __init__(self, stonks):
        self.stonks = stonks
        self.vantage_key = os.environ.get("ALPHAVANTAGE")

    @command(help="Get's ip data from domain or IP")
    async def ip(self, ctx, arg):
        rq = requests.get(f"http://ip-api.com/json/{arg}")
        out = json.loads(rq.content)
        if rq.status_code == 200:
            if "failed" in out["status"]:
                await ctx.send("Haku epäonnistui")
            elif "success" in out["status"]:
                haku = f"Country: {out['country']}\nRegion: {out['regionName']}\nCity: {out['city']}\nZip: {out['zip']}\nTimezone: {out['timezone']}\nOrg: {out['org']}\nIsp: {out['isp']}\nIp: {out['query']}"
                emb = discord.Embed(
                    title=arg,
                    description="Query for domain/ip",
                    color=discord.Color.blue(),
                )
                emb.add_field(name="Data", value=haku)
                await ctx.send(embed=emb)
        else:
            ctx.send("400 Bad request")

    @command(help="Shows server information")
    async def info(self, ctx):
        emb = discord.Embed(
            title=f"{ctx.guild.name}",
            description="Server Information",
            timestamp=datetime.utcnow(),
        )
        emb.add_field(
            name="Server created at",
            value=f"{ctx.guild.created_at.strftime('%d/%m/%Y %H:%M:%S')}",
            inline=False,
        )
        emb.add_field(name="Server Region", value=f"{ctx.guild.region}")
        emb.add_field(name="Server ID", value=f"{ctx.guild.id}")
        emb.add_field(
            name="Member count", value=f"{ctx.guild.member_count}", inline=False
        )
        emb.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=emb)

    @command(help="Shows user information")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        emb = discord.Embed(color=member.color, timestamp=datetime.utcnow())
        emb.set_author(name=f"User info - {member}")
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )
        emb.add_field(name="ID", value=member.id, inline=False)
        emb.add_field(
            name="Created at",
            value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            inline=False,
        )
        emb.add_field(
            name="Joined at",
            value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
            inline=False,
        )
        emb.add_field(
            name=f"Roles ({len(roles)})",
            value=" ".join([role.mention for role in roles]),
            inline=False,
        )
        emb.add_field(name="Top role:", value=member.top_role.mention, inline=False)
        await ctx.send(embed=emb)

    @command(help="Time now")
    async def now(self, ctx):
        y = datetime.now()
        x = y.strftime("%H:%M:%S, %d/%m/%Y")
        emb = discord.Embed(
            title="Time now", description=x
        )  # color=discord.Color.dark_red())
        emb.set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @command(help="PingPong!")
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send("Testing ping...")
        stop_time = time.time()
        await message.edit(
            content=f"Pong in {round(self.stonks.latency*1000)}ms!\nAPI latency: {round((stop_time - start_time) * 1000)}ms!"
        )

    @command(help="Bitcoin's current price")
    async def btc(self, ctx):
        btc = helpers.bitcoin()
        emb = discord.Embed(
            title="Bitcoin", description=btc, color=discord.Color.gold()
        )
        await ctx.send(embed=emb)

    @command(
        name="convert",
        help="Convert from one currency to another one i.e, -convert USD JPY.",
    )
    async def convert(self, ctx, from_currency, to_currency):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency,
            "to_currency": to_currency,
            "apikey": self.vantage_key,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    bucks = await response.json()
                    from_currency = bucks["Realtime Currency Exchange Rate"][
                        "1. From_Currency Code"
                    ]
                    to_currency = bucks["Realtime Currency Exchange Rate"][
                        "3. To_Currency Code"
                    ]
                    exchange_rate = bucks["Realtime Currency Exchange Rate"][
                        "5. Exchange Rate"
                    ]
                    embed = discord.Embed(color=discord.Color.purple())
                    embed.add_field(
                        name="Conversion",
                        value=f"**1 {from_currency} is {exchange_rate} {to_currency}**",
                        inline=False,
                    )

                    await ctx.reply(embed=embed)
                else:
                    await ctx.send(f"No company found!")


def setup(stonks):
    stonks.add_cog(Utils(stonks))