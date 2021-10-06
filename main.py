from discord.ext import commands, tasks
import discord
import os


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')  # disabling discord.py default help command


@bot.event
async def on_ready():
    # printing ready once bot has established connection with discord servers
    print('adrianscamhouse')

bot.load_extension('cogs.misc')
bot.load_extension('cogs.games')

try:
    bot.run(os.environ.get('powerbot_key'))
except:
    print('unable to connect')
