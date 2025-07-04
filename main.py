import discord
from discord.ext import commands
from json import load
import os
from dotenv import load_dotenv
from pathlib import Path
from logging import WARN

from cogs.ui.report_bug_ui import BugReportButtons, BugActionButtons
from cogs.ui.ticket_ui import TicketMenuView, TicketButtons

load_dotenv()
with open("config.json", "r", encoding="utf-8") as file:
    config = load(file)


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="?", intents=intents, help_command=None)

        self.cogslist = [".".join(file.relative_to("cogs").with_suffix("").parts) for file in Path("cogs").rglob("*.py") if not file.name.startswith("__")]

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error

    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension("cogs."+cog)

    async def on_ready(self):
        self.add_view(TicketMenuView(self))
        self.add_view(TicketButtons(self))
        self.add_view(BugReportButtons(self))
        self.add_view(BugActionButtons(self))
        await self.tree.sync()
        os.system("cls" if os.name == "nt" else "clear")
        print("")


if __name__ == "__main__":
    client = Client()
    client.run(os.getenv("TOKEN"), log_level=WARN)