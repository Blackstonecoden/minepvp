import os
from dotenv import load_dotenv
from json import load
from pathlib import Path
from logging import WARN

import discord
from discord.ext import commands

load_dotenv()
with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/disabled', intents=intents, help_command=None)

        self.cogslist = ['.'.join(file.relative_to('cogs').with_suffix('').parts) for file in Path('cogs').rglob('*.py') if not file.name.startswith('__')]

    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension("cogs."+cog)

    async def on_ready(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        global_commands = await self.tree.sync()
        #guild_commands = await self.tree.sync(guild=discord.Object(id=config["admin_guild_id"]))
        #await client.change_presence(activity = discord.CustomActivity(name=config["custom_app_status"]))

if __name__ == "__main__":
    client = Client()
    client.run(os.getenv('TOKEN'), log_level=WARN)