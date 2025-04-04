import discord
from discord.ext import commands
from json import load
from time import time

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class messages_log(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        
        channel = message.guild.get_channel(config["channels"]["messages_log"])
        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["message_circle"]} MESSAGE DELETED",
            description=f"""
            > **User Information**
            > - Ping: <@{message.author.id}>
            > - Username: `{message.author.name}`

            > **Message Information**
            > - Location: <#{message.channel.id}>
             
            Timestamp: <t:{int(time())}:D>
            """,
            color=0xda373c)
        embed.set_thumbnail(url=message.author.display_avatar.url)
        embed.set_image(url="attachment://line.png")
        content_embed = discord.Embed(
            title=f"{config["emojis"]["file_text"]} MESSAGE CONTENT",
            description=f"""```{message.content}```""",
            color=0xda373c)       
        content_embed.set_image(url="attachment://line.png")     
        await channel.send(embeds=[embed, content_embed], file=line)

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.bot:
            return
        
        channel = after.guild.get_channel(config["channels"]["messages_log"])
        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["message_circle"]} MESSAGE EDITED",
            description=f"""
            > **User Information**
            > - Ping: <@{after.author.id}>
            > - Username: `{after.author.name}`

            > **Message Information**
            > - Location: <#{after.channel.id}>
            > - Link: {after.jump_url}
            
            Timestamp: <t:{int(time())}:D>
            """,
            color=0xfee75c)
        embed.set_thumbnail(url=after.author.display_avatar.url)
        embed.set_image(url="attachment://line.png")
        content_before_embed = discord.Embed(
            title=f"{config["emojis"]["file_text"]} MESSAGE CONTENT BEFORE",
            description=f"""```{before.content}```""",
            color=0xfee75c)       
        content_before_embed.set_image(url="attachment://line.png")     
        content_after_embed = discord.Embed(
            title=f"{config["emojis"]["file_text"]} MESSAGE CONTENT AFTER",
            description=f"""```{after.content}```""",
            color=0xfee75c)       
        content_after_embed.set_image(url="attachment://line.png")   
        await channel.send(embeds=[embed, content_before_embed, content_after_embed], file=line)
            
async def setup(client:commands.Bot) -> None:
    await client.add_cog(messages_log(client))