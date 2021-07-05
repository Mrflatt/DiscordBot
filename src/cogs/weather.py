import discord
import os
import asyncio
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import command
from dotenv import load_dotenv
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit


load_dotenv()
yahoo_client_id = os.environ.get("YAHOO_CLIENT_ID")
yahoo_secret = os.environ.get("YAHOO_SECRET")
app_id = os.environ.get("YAHOO_ID")

data = YahooWeather(APP_ID=app_id, api_key=yahoo_client_id, api_secret=yahoo_secret)


class Weather(commands.Cog):
    """Shows weather on requested place"""

    def __init__(self, stonks):
        self.stonks = stonks

    @command(name="weather", help="Weather info")
    async def get_weather(self, ctx, city: str):
        emb = weather_query(city)
        emb.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def weather_today(self):
        await self.stonks.wait_until_ready()
        channel = self.stonks.get_channel(794886689654177792)
        while not self.stonks.is_closed():
            now_hour = datetime.now().hour
            now_minute = datetime.now().minute
            if now_hour == 10 and now_minute == 00:
                emb = weather_query("kotka")
                emb.set_footer(text=f"Requested automatic by {self.stonks.name}")
                await channel.send(f"It's going to be beautiful day!")
                await channel.send(embed=emb)
                time_ = 90
            elif now_hour == 16 and now_minute == 15:
                emb = weather_query("kotka")
                emb.set_footer(text=f"Requested automatic by {self.stonks.name}")
                await channel.send(f"Weather now!")
                await channel.send(embed=emb)
                time_ = 90
            else:
                time_ = 10
            await asyncio.sleep(time_)


def setup(stonks):
    stonks.add_cog(Weather(stonks))


def weather_query(city):
    data.get_yahoo_weather_by_city(f"{city.lower()}", Unit.celsius)
    country = data.location.country
    avg_temp = data.condition.temperature
    temp_text = data.condition.text
    sunset = data.astronomy.sunset
    sunrise = data.astronomy.sunrise
    pressure = data.atmosphere.pressure
    wind_speed = data.atmosphere.visibility
    emb = discord.Embed(
        title=f"Weather in {city.capitalize()} {country.capitalize()}",
        timestamp=datetime.utcnow(),
        color=discord.Color.random(),
    )
    emb.add_field(name="Description", value=f"{temp_text}", inline=False)
    emb.add_field(name="Temperature(°C)", value=f"{avg_temp}°C", inline=False)
    emb.add_field(name="Visibility(km)", value=f"{wind_speed}km", inline=False)
    emb.add_field(name="Pressure(hPa)", value=f"{pressure}hPa", inline=False)
    emb.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
    return emb
