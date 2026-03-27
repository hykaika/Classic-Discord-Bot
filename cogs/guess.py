import discord
from discord.ext import commands
import random
import asyncio

class GuessingGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guess')
    async def guess(self, ctx):
        number = random.randint(1, 50)
        await ctx.send("I'm thinking of a number between **1 and 50**. You have 5 attempts!")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

        for i in range(5):
            try:
                guess_msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess = int(guess_msg.content)

                if guess == number:
                    return await ctx.send(f"Correct! The number was **{number}**. You won!")
                elif guess < number:
                    await ctx.send("Higher!")
                else:
                    await ctx.send("Lower!")
            except asyncio.TimeoutError:
                return await ctx.send(f"Time is up! The number was {number}.")

        await ctx.send(f"Game over! The number was **{number}**.")

async def setup(bot):
    await bot.add_cog(GuessingGame(bot))