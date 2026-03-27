import discord
from discord.ext import commands
import json
import os

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'levels.json'
        self.users = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        user_id = str(message.author.id)
        
        if user_id not in self.users:
            self.users[user_id] = {'xp': 0, 'level': 0}

        old_level = self.users[user_id]['level']
        self.users[user_id]['xp'] += 10
        new_level = self.users[user_id]['xp'] // 100
        
        self.users[user_id]['level'] = new_level
        self.save_data()

        if new_level > old_level:
            channel_id = self.bot.config.get("level_channel_id")
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title="Level Up! 📈",
                    description=f"Congratulations {message.author.mention}, you reached **Level {new_level}**!",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)

    @commands.command(name='rank')
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        data = self.users.get(user_id, {'xp': 0, 'level': 0})
        
        embed = discord.Embed(title=f"Rank: {member.name}", color=discord.Color.blue())
        embed.add_field(name="Level", value=data['level'], inline=True)
        embed.add_field(name="XP", value=data['xp'], inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        sorted_users = sorted(self.users.items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
        
        description = ""
        for i, (user_id, stats) in enumerate(sorted_users, 1):
            user = self.bot.get_user(int(user_id))
            name = user.name if user else f"User {user_id}"
            description += f"**{i}. {name}** - Level {stats['level']} ({stats['xp']} XP)\n"

        embed = discord.Embed(title="Top 10 Leaderboard", description=description, color=discord.Color.gold())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot