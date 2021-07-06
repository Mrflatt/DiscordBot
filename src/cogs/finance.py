import requests
import urllib
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import json
import logging
import discord
import asyncio


class Finance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_task.start()

    @tasks.loop()
    async def status_task(self):
        await asyncio.sleep(2)
        response = requests.get("https://www.bitcoin.de")
        soup = BeautifulSoup(response.content, "html.parser")
        btc_price = soup.find(id="ticker_price").text

        await self.bot.change_presence(
            activity=discord.Game(f"BTC-Price: {btc_price}"),
            status=discord.Status.online,
        )

        await self.bot.change_presence(
            activity=discord.Game(f"Bitcoin: {btc_price}"), status=discord.Status.online
        )
        await asyncio.sleep(10)
        response = requests.get("https://www.bitcoin.de/de/etheur/market")
        soup = BeautifulSoup(response.content, "html.parser")
        ether_price = soup.find(id="ticker_price").text

        await self.bot.change_presence(
            activity=discord.Game(f"Ether-Price: {ether_price}"),
            status=discord.Status.online,
        )

        await self.bot.change_presence(
            activity=discord.Game(f"Ethereum: {ether_price}"),
            status=discord.Status.online,
        )

        await asyncio.sleep(10)
        response = requests.get("https://www.bitcoin.de/de/ltceur/market")
        soup = BeautifulSoup(response.content, "html.parser")
        ltc_price = soup.find(id="ticker_price").text

        await self.bot.change_presence(
            activity=discord.Game(f"LTC-Price: {ltc_price}"),
            status=discord.Status.online,
        )

        await self.bot.change_presence(
            activity=discord.Game(f"Litecoin: {ltc_price}"),
            status=discord.Status.online,
        )

        await asyncio.sleep(10)

    @commands.command(help="Bitcoin's current price")
    async def btc(self, ctx):
        btc = bitcoin()
        emb = discord.Embed(title="Bitcoin", color=discord.Color.gold())
        emb.add_field(
            name="USD",
            value=f"{btc[0]}$",
            inline=False,
        )
        emb.add_field(
            name="EUR",
            value=f"{btc[1]}€",
            inline=False,
        )
        emb.set_thumbnail(
            url="https://usethebitcoin.com/wp-content/uploads/2018/08/bitcoin-pic-main-500x500.png"
        )
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Finance(bot))


def bitcoin():
    response_eur = urllib.request.urlopen(
        "https://api.coindesk.com/v1/bpi/currentprice/EUR.json"
    )
    data = json.load(response_eur)
    return [f"{data['bpi']['USD']['rate']}", f"{data['bpi']['EUR']['rate']}"]
