import discord
from discord.ext import commands

class Autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_id = self.bot.config.get("member_role_id")
        role = member.guild.get_role(role_id)
        
        if role:
            await member.add_roles(role)
            print(f"Assigned {role.name} to {member.name}")
        else:
            print(f"Error: Role ID {role_id} not found.")

async def setup(bot):
    await bot.add_cog(Autorole(bot))