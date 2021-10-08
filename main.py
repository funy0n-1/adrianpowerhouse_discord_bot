from discord.ext import commands, tasks
import discord
import os
import psycopg2, psycopg2.extras
import urllib
import base64

db_pass = os.environ.get('powerbot_db_pass')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')  # disabling discord.py default help command

try:
    bot.database = psycopg2.connect(f"dbname='powerbot' user='postgres' host='localhost' password={db_pass}")
    print('########################### database opened')
except:
    print('unable to connect to database')


@bot.event
async def on_ready():
    cursor = bot.database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for i in bot.guilds:
        cursor.execute('SELECT EXISTS(SELECT * FROM servers WHERE guild_id=%s) AS "exists"', (str(i.id),))
        data = cursor.fetchone()
        print(data)
        if data['exists'] == False:
            cursor.execute('INSERT INTO servers (guild_id) VALUES (%s)', (i.id,))
            bot.database.commit()
            for user in i.members:
                if user.id != bot.user.id:
                    cursor.execute('INSERT INTO users (member_id, guild_id) VALUES (%s,%s)', (user.id, i.id))
                    bot.database.commit()
    cursor.close()
    print('########################### adrianpowerbot ready')

bot.load_extension('cogs.misc')
bot.load_extension('cogs.games')

try:
    bot.run(os.environ.get('powerbot_key'))
except:
    print('unable to connect')

print('########################### database closed')
bot.database.close()