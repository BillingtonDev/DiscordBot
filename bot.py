'''
Author: Micah
Description: Application to learn how to build bots in Python.
Source(s): https://realpython.com/how-to-make-a-discord-bot-python/#using-utility-functions
'''
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()  
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# Succesful connection message to terminal.
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# Greet new chat members
@bot.event
async def on_member_join(member):
    await member.create.dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

# Exception handeling on events    
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message:{args[0]}\n')
        else:
            raise

# Random Winston Churchill quote generator.
@bot.command(name='wc', help='Responds with a random quote from Winston Churchill.')
async def winston(ctx):
    wc_quotes = [
        "We shall never surrender",
        "Victory!",
        "Like putting your head in a lion's mouth!"
    ]
    
    response = random.choice(wc_quotes)
    await ctx.send(response)

# Dice simulator
@bot.command(name='roll_dice', help='Simulate rolling dice. Enter as !ctx num_dice num_sides.')
async def roll(ctx, num_dice: int, num_sides: int):
    dice = [
        str(random.choice(range(1, num_sides + 1)))
        for _ in range(num_dice)
    ]
    await ctx.send(', '.join(dice))
        
# Create new chats    
@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)   
      
# Handle admin exceptions on !create-channel  
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)