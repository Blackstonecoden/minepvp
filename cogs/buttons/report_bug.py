import discord
from discord.ext import commands
from discord import ui
from json import load, dump
import time

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)
with open("data/bug_reports.json", 'r') as file:
    bug_reports = load(file)

class BugReportButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=config["emojis"]["alert_triangle"], custom_id="report_bug")
    async def report_bug_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_modal(BugReportModal(self.client))


class BugReportModal(ui.Modal):
    def __init__(self, client: commands.Bot):
        super().__init__(title="Bug Report")
        self.client = client
    location = discord.ui.TextInput(label="Location", placeholder="Where did the bug occur?", min_length=2, max_length=25, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Description", placeholder="Describe the bug in detail.", max_length=500, style=discord.TextStyle.long)
    reproduction = discord.ui.TextInput(label="Steps To Reproduce", placeholder="How can we reproduce the bug?", max_length=500, style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        channel = interaction.guild.get_channel(config["channels"]["bug_reports"])

        line = discord.File("images/line.png")
        embed = discord.Embed(title=f"{config['emojis']['alert_triangle']} BUG REPORTED", 
                    description=f"""
                    **Bug Information**
                    > - User: <@{interaction.user.id}>
                    > - Location: `{self.location}`
                    """, 
                    color=0x56565d)
        embed.set_image(url="attachment://line.png")
        description = discord.Embed(description=f"**Bug Description**\n```{self.description}```", color=0x56565d)
        description.set_image(url="attachment://line.png")
        reproduction = discord.Embed(description=f"**Reproduction**\n```{self.reproduction}```", color=0x56565d)
        reproduction.set_image(url="attachment://line.png")

        message = await channel.send(embeds=[embed, description, reproduction], files=[line], view=BugActionButtons(self.client))

        self.client.bug_reports[str(message.id)] = {"reported_by": interaction.user.id,"created_at": int(time.time()), "content": {"location": self.location.value, "description": self.description.value, "reproduction": self.reproduction.value}}
        with open("data/bug_reports.json", 'w') as file:
            dump(self.client.bug_reports, file, indent=4)

class BugActionButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=config["emojis"]["check_green"], custom_id="accept_bug")
    async def accept_bug_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.send_modal(BugAcceptModal(self.client))

    @discord.ui.button(emoji=config["emojis"]["x_red"], custom_id="reject_bug")
    async def reject_bug_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
        del self.client.bug_reports[str(interaction.message.id)]
        with open("data/bug_reports.json", 'w') as file:
            dump(self.client.bug_reports, file, indent=4)

        embeds = []
        for embed in interaction.message.embeds:
            embed.color = 0xda373c
            embeds.append(embed)
        await interaction.message.edit(embeds=embeds, view=None, attachments=[])


class BugAcceptModal(ui.Modal):
    def __init__(self, client: commands.Bot):
        super().__init__(title="Bug Report")
        self.client = client
    bug_title = discord.ui.TextInput(label="Title", placeholder="Give the bug a proper title.", max_length=50, style=discord.TextStyle.short)
    bug_tag = discord.ui.TextInput(label="Tag", placeholder="Assign a tag to the bug.", max_length=25, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        bug_tag_id = config["bug_forum_tags"].get(self.bug_tag.value.lower(), {}).get("tag_id")
        if not bug_tag_id: 
            await interaction.response.send_message(f"❌ Invalid tag: `{self.bug_tag.value}`.", ephemeral=True)
            return
        
        await interaction.response.defer()

        content = self.client.bug_reports[str(interaction.message.id)]
        del self.client.bug_reports[str(interaction.message.id)]
        with open("data/bug_reports.json", 'w') as file:
            dump(self.client.bug_reports, file, indent=4)

        embeds = []
        for embed in interaction.message.embeds:
            embed.color = 0x248046
            embeds.append(embed)
        await interaction.message.edit(embeds=embeds, view=None, attachments=[])


        channel: discord.ForumChannel = interaction.guild.get_channel(config["channels"]["bug_forum"])
        tag = channel.get_tag(bug_tag_id)
        thread = await channel.create_thread(name=self.bug_title.value, applied_tags=[tag],
                              content=f"""**Bug Information**\n> - Location: `{tag.name}`\n> - Title `{self.bug_title.value}`\n> - User: <@{content["reported_by"]}>\n> - Reported at: <t:{content["created_at"]}:D>\n\n**Bug Description**\n```{content["content"]["description"]}```\n\n**Reproduction**\n```{content["content"]["description"]}```""")
        await thread.message.pin()
        


class report_bug_buttons(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.bug_reports = bug_reports


async def setup(client:commands.Bot) -> None:
    await client.add_cog(report_bug_buttons(client))