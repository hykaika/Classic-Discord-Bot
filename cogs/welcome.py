import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = self.bot.config.get("welcome_channel_id")
        channel = self.bot.get_channel(channel_id)
        
        if channel:
            embed = discord.Embed(
                title="Welcome to the Server! 🎉",
                description=f"Hello {member.mention}, we are glad to have you here!",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Member Count: {member.guild.member_count}")
            
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))