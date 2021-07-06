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
        await asyncio.sleep(10)
        response = requests.get("https://www.bitcoin.de/de/etheur/market")
        soup = BeautifulSoup(response.content, "html.parser")
        ether_price = soup.find(id="ticker_price").text
        await self.bot.change_presence(
            activity=discord.Game(f"Ether-Price: {ether_price}"),
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
        await asyncio.sleep(10)


def setup(bot):
    bot.add_cog(Finance(bot))


# response = urllib.request.urlopen(
#        "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
#     )
# response_eur = urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice/EUR.json")
# data = json.load(response)
# EUR = json.load(response_eur)
# print(data)
# print(EUR["bpi"]["EUR"]["rate"])
