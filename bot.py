import datetime
import discord
import pandas as pd
from dotenv import dotenv_values
from discord.ext import commands, tasks
from src.get_discounts import get_daily_discounts
from src.helpers import table_to_message

env = dotenv_values('.env')
token = env['TOKEN']

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
    if now > target_time and now < target_time + datetime.timedelta(minutes=5):
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

    print(f"Number of subscribers: {len(subscribers)}")
    await ctx.author.send(f"Subscribed! You are cool :)\n"
                          f"{get_daily_discounts(datetime.datetime.now() - datetime.timedelta(hours=7))}")


@bot.command()
async def unsubscribe(ctx):
    print(f"{ctx.author} is trying to unsubscribe")
    try:
        subscribers = pd.read_csv('subscribers.csv')['subscribers']
        if ctx.author.id not in subscribers.values:
            await ctx.author.send("You are not subscribed!")
            return
        subscribers = subscribers[~subscribers.isin([ctx.author.id])]
        subscribers.to_csv('subscribers.csv', index=False)
        await ctx.author.send("Unsubscribed! You are mean :(")
    except FileNotFoundError:
        await ctx.author.send("You are not subscribed!")
        return


@bot.command()
async def all_deals(ctx):
    print(f"{ctx.author} is trying to get all deals")
    deals = pd.read_csv('deals.csv')
    message = table_to_message(deals)
    if message == '':
        message = 'No deals available :('
    else:
        message = "All possible deals:\n" + message
    
    await ctx.author.send(message)


@bot.command()
async def elp(ctx):
    print(f"{ctx.author} is trying to get help")
    await ctx.author.send("```\n"
                          "Commands:\n"
                          "!subscribe - Subscribe to daily discounts\n"
                          "!unsubscribe - Unsubscribe from daily discounts\n"
                          "!help - Get help\n"
                          "!all_deals - Get all possible deals (whether they apply today or not)\n"
                          "```")


@bot.command()
async def admin_message(ctx, *message):
    print(f"{ctx.author} is trying to send a message to all subscribers")
    admin_id = env['ADMIN_ID']
    if str(ctx.author.id) == admin_id:
        subscribers = pd.read_csv('subscribers.csv')['subscribers']
        for subscriber in subscribers:
            user = bot.get_user(subscriber)
            await user.send(" ".join(message))
        await ctx.author.send("Message sent to all subscribers!")
    else:
        await ctx.author.send("You are not authorized to send messages to all subscribers!")


bot.run(token)