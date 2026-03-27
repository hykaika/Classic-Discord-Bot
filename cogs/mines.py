import discord
from discord.ext import commands
import random

class Mines(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mines')
    async def mines(self, ctx, bombs: int = 3):
        if bombs < 1 or bombs > 10:
            return await ctx.send("Please choose between 1 and 10 bombs.")

        size = 5
        grid = [['??' for _ in range(size)] for _ in range(size)]
        
        # Place bombs
        count = 0
        while count < bombs:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            if grid[y][x] == '??':
                grid[y][x] = 'X'
                count += 1

        # Convert to emojis
        display = ""
        for row in grid:
            for cell in row:
                if cell == 'X':
                    display += "||💣|| "
                else:
                    display += "||✅|| "
            display += "\n"

        embed = discord.Embed(
            title="Minesweeper",
            description=f"Click the spoilers to reveal the field!\n\n{display}",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mines(bot))