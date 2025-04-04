import discord
from discord.ext import commands
from json import load
from time import time

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class join_leave_log(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(config["channels"]["join_leave_log"])
        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["users"]} MEMBER JOINED",
            description=f"""
            > **User Information**
            > - Ping: <@{member.id}>
            > - Username: `{member.name}`
            > - Account age: <t:{int(member.created_at.timestamp())}:R>
             
            Timestamp: <t:{int(time())}:D>
            """,
            color=0x248046)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="attachment://line.png")
        await channel.send(embed=embed, file=line)

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        channel = member.guild.get_channel(config["channels"]["join_leave_log"])
        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["users"]} MEMBER LEFT",
            description=f"""
            > **User Information**
            > - Ping: <@{member.id}>
            > - Username: `{member.name}`
            > - Account age: <t:{int(member.created_at.timestamp())}:R>
             
            Timestamp: <t:{int(time())}:D>
            """,
            color=0xda373c)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="attachment://line.png")
        await channel.send(embed=embed, file=line)
            
async def setup(client:commands.Bot) -> None:
    await client.add_cog(join_leave_log(client))