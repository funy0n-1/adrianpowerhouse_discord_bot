import psycopg2, psycopg2.extras

class inventory:
    async def get(id):
        pass

class user:
    async def add(bot, member):
        cursor = bot.database.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT EXISTS(SELECT * FROM users WHERE member_id=%s AND guild_id=%s) AS exists', (member.id, member.guild.id))
        exists = cursor.fetchone()
        if exists['exists'] == False:
            cursor.execute('INSERT INTO users (member_id, guild_id) VALUES (%s, %s)', (member.id, member.guild.id))
            bot.database.commit()
            return True
        else:
            return True
        cursor.close()