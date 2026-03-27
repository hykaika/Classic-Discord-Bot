import discord
from discord.ext import commands
import json
import os

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'users.json'
        self.user_db = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_db, f, indent=4)

    def register_user(self, member):
        user_id = str(member.id)
        if user_id not in self.user_db:
            self.user_db[user_id] = {
                "name": member.name,
                "bio": "No bio set.",
                "balance": 0,
                "joined_at": str(member.joined_at)[:10]
            }
            self.save_data()

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.purple())
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created at", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        self.register_user(member)
        
        data = self.user_db[user_id]
        
        embed = discord.Embed(title=f"User Info: {member.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Bio", value=data["bio"], inline=False)
        embed.add_field(name="Balance", value=f"{data['balance']} Coins", inline=True)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%d.%m.%Y"), inline=True)
        embed.add_field(name="Joined Server", value=data["joined_at"], inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='setbio')
    async def setbio(self, ctx, *, bio_text: str):
        user_id = str(ctx.author.id)
        self.register_user(ctx.author)
        
        if len(bio_text) > 100:
            return await ctx.send("Bio is too long! (Max 100 characters)")

        self.user_db[user_id]["bio"] = bio_text
        self.save_data()
        await ctx.send("Biography updated!")

async def setup(bot):
    await bot.add_cog(Utility(bot))