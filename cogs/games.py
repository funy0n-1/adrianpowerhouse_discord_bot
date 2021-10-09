from discord.ext import commands
import discord
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
        response1 = False
        response2 = False
        players = []
        players.append(ctx.message.author.id)
        timeout = 15
        time_stop = time.time() + timeout
        def check(msg):
            return str(msg.content).lower().startswith('join')
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
                break
        if len(players) > 1:
            player1 = self.bot.get_user(players[0])
            player2 = self.bot.get_user(players[1])
            async def private_channel(user):
                overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True),
                }
                channel = await ctx.guild.create_text_channel(user.name, overwrites=overwrites)
                return channel
            
            player1_channel = await private_channel(player1)
            player2_channel = await private_channel(player2)

            def rps1(msg):
                if str(msg.content).startswith('r') or str(msg.content).startswith('p') or str(msg.content).startswith('s') and msg.channel == player1_channel and msg.author == player1:
                    return True
                else:
                    return False

            def rps2(msg):
                if str(msg.content).startswith('r') or str(msg.content).startswith('p') or str(msg.content).startswith('s') and msg.channel == player2_channel and msg.author == player2:
                    return True
                else:
                    return False

            await player1_channel.send(f'{player1.mention} \n type \n R for rock, \n P for paper, \n S for scissors \n you have 15 seconds to respond.')
            await player2_channel.send(f"{player2.mention} \n awaiting {player1.name}'s response.")
            try:
                response1 = await self.bot.wait_for('message', timeout=15, check=rps1)
            except:
                await player1_channel.send(f'{player1.mention} 15 seconds over \n game cancelled')
                await player2_channel.send(f'{player2.mention} \n {player1.name} did not respond in time \n the game has been cancelled')
            if response1 != False:
                print('AAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH###########################')
                await player2_channel.send(f"{player2.mention} \n {player1.name} has entered their response \n type \n R for rock, \n P for paper, \n S for scissors \n you have 15 seconds to respond.")
                try:
                    response2 = await self.bot.wait_for('message', timeout=15, check=rps2())
                except:
                    await player2_channel.send(f'{player2.mention} 15 seconds over \n game cancelled')
                    await player1_channel.send(f'{player1.mention} \n {player2.name} did not respond in time \n the game has been cancelled')
            if response2:
                def win_check(r1, r2):
                    if r1 == r2:
                        return False
                    elif r1 == 'r':
                        if r2 == 'scissors':
                            return r1
                        else:
                            return r2
                    elif r1 == 'p':
                        if r2 == 'r':
                            return r1
                        else:
                            return r2
                    elif r1 == 's':
                        if r2 == 'p':
                            return r1
                        else:
                            return r2

                win_res = win_check(response1, response2)
                if win_res:
                    if win_res == response1:
                        await player1_channel.send(f"{player1.mention} \n You win!")
                        await player2_channel.send(f"{player2.mention} \n You lost loser!")
                        pass
                    else:
                        await player2_channel.send(f"{player2.mention} \n You win!")
                        await player1_channel.send(f"{player1.mention} \n You lost loser!")

                else:
                    await player1_channel.send("it's a draw!")
                    await player2_channel.send("it's a draw!")
            del_time = time.time() + 25
            while(time.time() < del_time):
                pass
            await player1_channel.delete()
            await player2_channel.delete()

        else:
            await ctx.send('there must be 2 players in game to start')

def setup(bot):
    bot.add_cog(games(bot))
