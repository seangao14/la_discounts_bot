import datetime
import discord
import pandas as pd
from config import token
from discord.ext import commands, tasks
from src.get_discounts import get_discounts

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    schedule_message.start()

@tasks.loop(seconds=10)
async def schedule_message():
    now = datetime.datetime.now()
    target_time = now.replace(hour=19, minute=21, second=0, microsecond=0)
    if now > target_time and now < target_time + datetime.timedelta(minutes=120):
        message = get_discounts()
        
        subscribers = pd.read_csv('subscribers.csv')['subscribers']
        for subscriber in subscribers:
            user = bot.get_user(subscriber)

            await user.send(message)

@bot.command()
async def subscribe(ctx):
    try:
        subscribers = pd.read_csv('subscribers.csv')['subscribers']
        if ctx.author.id in subscribers.values:
            await ctx.author.send("You are already subscribed!")
            return
    except FileNotFoundError: # initialize subscribers.csv if it doesn't exist
        subscribers = pd.DataFrame(columns=['subscribers'])
        subscribers.loc[0] = [ctx.author.id]
        subscribers.to_csv('subscribers.csv', index=False)
        await ctx.author.send(f"Subscribed!, your id is {ctx.author.id}")
        return
    
    await ctx.author.send(f"Subscribed!, your id is {ctx.author.id}")
    subscribers.loc[len(subscribers)] = ctx.author.id
    subscribers.to_csv('subscribers.csv', index=False)

bot.run(token)