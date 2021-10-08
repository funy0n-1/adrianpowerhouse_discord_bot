from discord.ext import commands
import time, random

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roulette(self, ctx):
        def check(msg):

            data = str(msg.content).lower()
            return data.startswith('join')
        timeout = 15
        time_loop = time.time() + timeout
        players = []
        players.append(ctx.message.author.id)
        await ctx.send(f"The roulette game has started! say 'join' to play. \n game starting in {timeout} seconds")
        while time.time() < time_loop:
            try:
                message = False
                message = await self.bot.wait_for('message', timeout=5, check=check)
            except:
                pass
            if message:
                if message.author.id not in players:
                    await ctx.send(message.author.name + " has joined the game.")
                    players.append(message.author.id)
                else:
                    await ctx.send(message.author.name + " is already in the game.")
        if len(players) > 1:
            loser_id = random.choice(players)
            loser = ctx.message.guild.get_member(int(loser_id))
            await ctx.send(loser.mention + " lost")
        else:
            await ctx.send('there needs to be at least 2 players in game')

    @commands.command()
    async def rps(self, ctx):
        players = []
        players.append(ctx.message.author.id)
        timeout = 15
        time_stop = time.time() + timeout
        def check(msg):
            return str(msg.content).startswith('join')
        await ctx.send(ctx.message.author.mention + " has started a game of rock paper scissors \n type 'join' to play against them")
        while time.time() < time_stop:
            message = False
            try:
                message = await self.bot.wait_for('message', timeout=5, check=check)
            except:
                pass
            if message:
                if message.author.id not in players and len(players) < 2:
                    players.append(message.author.id)
                else:
                    await ctx.send(message.author.mention + " is already in game or game is full.")
        if len(players) > 1:
            player1 = self.bot.get_user(players[0])
            player2 = self.bot.get_user(players[1])
            def rps(msg, member):
                if str(msg.content).startswith('r') or str(msg.content).startswith('p') or str(msg.content).startswith('s') and msg.author == member:
                    return True
                else:
                    return False
            await player1.send('type \n R for rock, \n P for paper, \n S for scissors \n you have 15 seconds to respond.')
            await player2.send(f"awaiting {player2.name}'s response.")
            try:
                message = self.bot.wait_for('message', timeout=15, check=rps(player1))
            except:
                await player2.send(f'{player1.name} did not respond \n game cancelled')


        else:
            await ctx.send('there must be 2 players in game to start')


def setup(bot):
    bot.add_cog(games(bot))
