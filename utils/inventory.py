import psycopg2
async def get_inventory(bot, user_id):
    cmd = bot.database.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cmd.execute('SELECT id FROM items WHERE name = %s LIMIT 1', (user_id,))
    #inventory = cmd.fetchone()