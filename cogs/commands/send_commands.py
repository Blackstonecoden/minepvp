import discord
from discord.ext import commands
from discord import app_commands
from json import load

with open("config.json", "r", encoding="utf-8") as file:
    config = load(file)


class send_commands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    send_command = app_commands.Group(name="send", description="Send custom messages", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    @send_command.command(name="guidelines", description="Send the guidelines embed in this channel")
    async def send_rules(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅", ephemeral=True)
        top_image = discord.File("images/banners/guidelines.png")
        top_embed = discord.Embed(color=0x6d6f78)
        top_embed.set_image(url="attachment://guidelines.png")

        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["book"]} DISCORD RULES",
            description=f"""
            > **What happens if a user breaks a rule?**  
            > Open a ticket in <#{config["channels"]["ticket_support"]}> to report them.\n> Make sure to provide valid evidence, such as screenshots.  

            > **How is this server moderated?**  
            > Breaking the rules may result in a timeout or a warning.\n> Severe violations can lead to a ban. \n> Ignorance of the rules does not exempt you from consequences.  

            > **We follow Discord's Terms**  
            > - [Discord Guidelines](https://discordapp.com/guidelines)  
            > - [Discord Terms](https://discordapp.com/terms)  
            """,
            color=0x6d6f78
        )
        embed.set_image(url="attachment://line.png")

        api_embed = discord.Embed(
            title=f"{config["emojis"]["box"]} MINECRAFT SERVER RULES",
            description=f"""
            > These are general rules that apply to all our Minecraft servers. Specific rules may vary between servers.

            > **Summary of the rules**  
            > - No hacking  
            > - No unfair advantages*  
            > - No duping  
            > - No swearing**  
            
            > -# *Unfair advantages include client modifications or texture packs that provide an unfair edge. If unsure, ask in the support chat.
            > 
            > -# **Swearing includes any form of insults. 
            """,
            color=0x6d6f78
        )
        api_embed.set_image(url="attachment://line.png")

        chat_rules_embed = discord.Embed(
            title=f"{config["emojis"]["message_circle"]} CHAT RULES",
            description=f"""
            > Just because something isn't listed here doesn't mean you can't be banned for it. Use common sense and stay out of trouble."

            > **Summary of the chat rules**  
            > - No swearing  
            > - No harassment  
            > - Absolutely no NSFW or suggestive content  
            > - No advertising  
            > - No spamming  
            > - No political discussions  
            > - Use common sense  
            """,
            color=0x6d6f78
        )
        chat_rules_embed.set_image(url="attachment://line.png")

        await interaction.channel.send(embeds=[top_embed, embed, api_embed, chat_rules_embed], files=[top_image, line])

    @send_command.command(name="join", description="Send the how to join embed in this channel")
    async def send_rules(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅", ephemeral=True)
        top_image = discord.File("images/banners/how_to_join.png")
        top_embed = discord.Embed(color=0x6d6f78)
        top_embed.set_image(url="attachment://how_to_join.png")

        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["play_circle"]} HOW TO JOIN",
            description=f"""
            > **Java**  
            > IP: `minepvp.net`
            > Port: `25565`

            > **Bedrock**  
            > IP: `bedrock.minepvp.net`
            > Port: `49196`

            > **Cracked**
            > IP: `cracked.minepvp.net`
            > Port: `25565`

            > **Minehut**
            > Comming soon...
            """,
            color=0x6d6f78)
        embed.set_image(url="attachment://line.png")

        await interaction.channel.send(embeds=[top_embed, embed], files=[top_image, line])

    @send_command.command(name="application", description="Send the application embed in this channel")
    async def send_rules(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅", ephemeral=True)
        top_image = discord.File("images/banners/application.png")
        top_embed = discord.Embed(color=0x6d6f78)
        top_embed.set_image(url="attachment://application.png")

        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["file_text"]} APPLICATION",
            description=f"""
            > **Information**
            > Are you passionate about Minecraft and would like to join the MinePvP staff team? We're looking for dedicated people to join our staff team! If you're ready, check out the **[MinePvP Staff Application](https://docs.google.com/forms/d/1cQ6OhTxPGdB_-ld71pKk9XsFhxkg4go29I0tnti7li4/edit)** to apply.

            > **Requirements**
            > - Must be at least 15 years old
            > - Understanding of the MinePvP community
            > - Basic understanding of moderation
            > - A genuine interest in helping the community
            """,
            color=0x6d6f78)
        embed.set_image(url="attachment://line.png")

        await interaction.channel.send(embeds=[top_embed, embed], files=[top_image, line])

async def setup(client:commands.Bot) -> None:
    await client.add_cog(send_commands(client))