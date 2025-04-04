import discord
from discord.ext import commands
from discord import app_commands
from json import load

from cogs.ui.ticket_ui import CloseConfirmButtons

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class close_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
     
    @app_commands.command(name="close", description="Closes the current ticket")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    async def close_ticket(self, interaction: discord.Interaction):
        channel = interaction.channel
        if str(channel.id) in self.client.ticket_list:
            line = discord.File("images/line.png")
            embed = discord.Embed(
                description=f"""
                ## Close Ticket
                Are you sure you want to close this ticket? Click the red button below if you want to close it.
                """,
                color=0xda373c)
            embed.set_image(url="attachment://line.png")
            view = CloseConfirmButtons(self.client)
            await interaction.response.send_message(embed=embed, files=[line], view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ You are not ticket staff", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(close_command(client))