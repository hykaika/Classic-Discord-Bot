import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll')
    async def roll(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(f'Results: {result}')
        except Exception:
            await ctx.send('Format has to be NdN! (e.g. 1d6)')

    @commands.command(name='8ball')
    async def eightball(self, ctx, *, question):
        responses = [
            'It is certain.', 'Outlook good.', 'Better not tell you now.',
            'Very doubtful.', 'No way.', 'Concentrate and ask again.'
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(name='coinflip')
    async def coinflip(self, ctx):
        outcome = random.choice(['Heads', 'Tails'])
        await ctx.send(f'🪙 The coin landed on: **{outcome}**')

async def setup(bot):
    await bot.add_cog(Fun(bot))