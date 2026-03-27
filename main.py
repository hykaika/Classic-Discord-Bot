import discord
import os
import asyncio
import json
from discord.ext import commands

with open('config.json', 'r') as f:
    config = json.load(f)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix=config["prefix"], intents=intents)
        self.config = config

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    async with bot:
        await bot.start(config["token"])

if __name__ == '__main__':
    asyncio.run(main())