import praw
import os
import random
import json
import urllib
from urllib import request
from dotenv import load_dotenv

load_dotenv()
user_id = os.environ.get('REDDIT_ID')
secret = os.environ.get('REDDIT_SECRET')
password = os.environ.get('REDDIT_PASSWORD')


def reddit_memes(subreddit_id):  # query to get reddit post from specific subreddit (UPDATE)
    reddit = praw.Reddit(client_id=user_id,
                         client_secret=secret,
                         user_agent='windows.com.bot.myredditbot:v1')
    submission = reddit.subreddit(subreddit_id).top()
    top = random.randint(1, 25)
    random_sub = ''
    for i in range(top):
        random_sub = next(x for x in submission if not x.stickied)
    # name = random_sub.title
    # em = discord.Embed(title=name, color=discord.Color.gold())
    # em.set_image(url=random_sub.url)
    return random_sub.url


def bitcoin():
    response = urllib.request.urlopen('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    data = json.load(response)
    return f'${data["bpi"]["USD"]["rate"]}'
