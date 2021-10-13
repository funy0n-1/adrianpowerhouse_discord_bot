class bot_admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def creat_item(self, ctx):
        def check(msg):
            if msg.channel == ctx.message.channel and msg.author == ctx.message.author:
                return True
            else:
                return False
        async def get_message(self, ctx):
            try:
                message = await self.bot.wait_for('message', timeout=60, check=check)
                return message
            except:
                await ctx.send('you took too long \n item creation cancelled')
                return False

        await ctx.send('please type the name of the item you wold like to create.')
        message = await get_message()
        if message:
            item_name = message.content
        

def setup(bot):
    bot.add_cog(bot_admin(bot))