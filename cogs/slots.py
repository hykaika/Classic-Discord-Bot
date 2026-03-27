import discord
from discord.ext import commands
import random
import json

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='slots')
    async def slots(self, ctx, amount: int):
        with open('users.json', 'r') as f:
            data = json.load(f)
        
        user_id = str(ctx.author.id)
        if amount <= 0 or data.get(user_id, {}).get('balance', 0) < amount:
            return await ctx.send("Insufficient balance or invalid amount!")

        emojis = "🍎🍊🍇💎🔔"
        a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
        
        slot_machine = f"**[ {a} | {b} | {c} ]**"
        
        if a == b == c:
            win = amount * 5
            data[user_id]['balance'] += win
            result = f"JACKPOT! You won **{win} Coins**!"
        elif a == b or b == c or a == c:
            win = amount * 2
            data[user_id]['balance'] += win
            result = f"Small win! You won **{win} Coins**!"
        else:
            data[user_id]['balance'] -= amount
            result = f"You lost **{amount} Coins**."

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Slot Machine", description=f"{slot_machine}\n\n{result}", color=discord.Color.gold())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Slots(bot))