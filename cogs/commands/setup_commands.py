import discord
from discord.ext import commands
from discord import app_commands
from json import load

from cogs.ui.report_bug_ui import BugReportButtons
from cogs.ui.ticket_ui import TicketMenuView

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class setup_commands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    setup_command = app_commands.Group(name="setup", description="Setup command", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    @setup_command.command(name="ticket", description="Setup the ticket system in this channel")
    async def setup_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅", ephemeral=True)
        top_image = discord.File("images/banners/ticket_support.png")
        top_embed = discord.Embed(color=0x56565d)
        top_embed.set_image(url="attachment://ticket_support.png")

        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["mail"]} TICKET SUPPORT",
            description="""
            > **Ticket Support Information**
            > - Response time is 0-48 hours.
            > - Only use tickets for appropriate issues
            > - Misusing this system can have consequences
            
            > **How to open a ticket?**
            > - Click the menu below and choose the category that fits your issue
            > - A ticket channel will open for you
            > - Please be patient until a team member responds.
            """,
            color=0x56565d)
        embed.set_image(url="attachment://line.png")
        await interaction.channel.send(embeds=[top_embed, embed], files=[top_image, line], view=TicketMenuView(self.client))

    @setup_command.command(name="bug", description="Setup the bugreport system in this channel")
    async def setup_bug(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅", ephemeral=True)
        top_image = discord.File("images/banners/bug.png")
        top_embed = discord.Embed(color=0x56565d)
        top_embed.set_image(url="attachment://bug.png")

        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["alert_triangle"]} BUG REPORT", 
            description="""
            > **BUG REPORT INFORMATION**
            > - Your bug will be reviewed by the team
            > - Report bugs for a better gameplay experience
            > - Do NOT use this feature to spam, otherwise, there will be consequences.
            
            > **HOW TO SUBMIT A BUG REPORT?**
            > - Click the button below to submit a bug report
            > - Please be patient until a team member reviews your report
            """, 
            color=0x56565d)
        embed.set_image(url="attachment://line.png")
        await interaction.channel.send(embeds=[top_embed, embed], files=[top_image, line], view=BugReportButtons(self.client))
    
async def setup(client:commands.Bot) -> None:
    await client.add_cog(setup_commands(client))