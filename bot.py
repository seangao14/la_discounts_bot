import datetime
import discord
import pandas as pd
from dotenv import dotenv_values
from discord.ext import commands, tasks
from src.get_discounts import get_daily_discounts

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    daily_message.start()

@tasks.loop(minutes=5)
async def daily_message():
    # -7 from UTC to PST
    now = datetime.datetime.now() - datetime.timedelta(hours=7)
    target_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now > target_time and now < target_time + datetime.timedelta(minutes=120):
        message = get_daily_discounts(now)
        
        subscribers = pd.read_csv('subscribers.csv')['subscribers']
        for subscriber in subscribers:
            user = bot.get_user(subscriber)

            await user.send(message)

@bot.command()
async def subscribe(ctx):
    print(f"{ctx.author} is trying to subscribe")
    try:
        subscribers = pd.read_csv('subscribers.csv')['subscribers']
        if ctx.author.id in subscribers.values:
            await ctx.author.send("You are already subscribed!")
            return
        subscribers.loc[len(subscribers)] = ctx.author.id
        subscribers.to_csv('subscribers.csv', index=False)

    except FileNotFoundError: # initialize subscribers.csv if it doesn't exist
        subscribers = pd.DataFrame(columns=['subscribers'])
        subscribers.loc[0] = [ctx.author.id]
        subscribers.to_csv('subscribers.csv', index=False)

    await ctx.author.send(f"Subscribed!:\n"
                          f"{get_daily_discounts(datetime.datetime.now() - datetime.timedelta(hours=7))}")

env = dotenv_values('.env')
token = env['TOKEN']

bot.run(token)