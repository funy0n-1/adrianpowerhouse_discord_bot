from discord.ext import commands


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test')

def setup(bot):
    bot.add_cog(misc(bot))
