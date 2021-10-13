from discord.ext import commands
import discord
import time, random

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx):
        players = []
        player_responses = []
        player_channels = []
        players.append(ctx.message.author)
        await ctx.send(f"{ctx.message.author.mention} has started a game of rock paper scissors! \n type 'join' to play against them! \n you have 15 seconds")
        def win_check(responses):
            print(responses)
            if responses[0] == responses[1]:
                return 'draw'
            elif responses[0] == 'r':
                if responses[1] == 's':
                    return 0
                else:
                    return 1
            elif responses[0] == 'p':
                if responses[1] == 'r':
                    return 0
                else:
                    return 1
            elif responses[0] == 's':
                if responses[1] == 'p':
                     return 0
                else:
                    return 1

        async def private_channel(user):
                overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True),
                }
                channel = await ctx.guild.create_text_channel(user.name, overwrites=overwrites)
                return channel
        async def get_response(player_channel):
            def rps_check(msg):
                if msg.channel == player_channel:
                    if str(msg.content).lower().startswith('r') or str(msg.content).lower().startswith('p') or str(msg.content).lower().startswith('s'):
                        return True
                    else:
                        return False
                else:
                    return False
            
            response = await self.bot.wait_for('message', timeout=15, check=rps_check)
            return response.content
        def join_check(msg):
            if str(msg.content).lower().startswith('join'):
                return True
            else:
                return False
        loop_time = time.time() + 15
        while time.time() < loop_time:
            message = None
            try:
                message = await self.bot.wait_for('message', timeout=5, check=join_check)
            except:
                pass
            if message is not None:
                if message.author is not self.bot.user and message.author not in players: ################################################
                    if len(players) < 2:
                        players.append(message.author)
                elif message.author in players:
                    await ctx.send("You're already in game.")
            if len(players) > 1:
                break
        if len(players) > 1:
            for i in players:
                player_channels.append(await private_channel(i))

            await player_channels[0].send('type \n r for rock \n p for paper \n s for scissors \n you have 15 seconds to respond')
            player_responses.append(await get_response(player_channels[0]))
            await player_channels[1].send('type \n r for rock \n p for paper \n s for scissors \n you have 15 seconds to respond')
            player_responses.append(await get_response(player_channels[1]))
            
            winner = win_check(player_responses)
            print(winner)
            if winner == 'draw':

                for i in player_channels:
                    await i.send("it's a draw!")
            elif winner == 0:
                for i in player_channels:
                    await i.send(f"{players[winner].name} has won!")
            elif winner == 1:
                for i in player_channels:
                    await i.send(f"{players[winner].name} has won!")
            wait_time = time.time() + 25
            while time.time() < wait_time:
                pass
            for i in player_channels:
                await i.delete()
            
            

def setup(bot):
    bot.add_cog(games(bot))
