import discord
from discord.ext import commands
from json import load
from time import time

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class punishments_log(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_member_ban")
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        log = [entry async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban)]
        entry = log[0]
        channel = guild.get_channel(config["channels"]["punishments_log"])
        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["block"]} MEMBER BANNED",
            description=f"""
            > **User Information**
            > - Ping: <@{member.id}>
            > - Username: `{member.name}`
             
            > **Ban Information**
            > - Staff: <@{entry.user.id}>
            > - Reason: `{entry.reason}`

            Timestamp: <t:{int(time())}:D>
            """,
            color=0xda373c)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="attachment://line.png")
        await channel.send(embed=embed, file=line)

    @commands.Cog.listener("on_member_unban")
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        log = [entry async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban)]
        entry = log[0]
        channel = guild.get_channel(config["channels"]["punishments_log"])
        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["block"]} MEMBER UNBANNED",
            description=f"""
            > **User Information**
            > - Ping: <@{user.id}>
            > - Username: `{user.name}`
             
            > **Unban Information**
            > - Staff: <@{entry.user.id}>

            Timestamp: <t:{int(time())}:D>
            """,
            color=0x248046)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_image(url="attachment://line.png")
        await channel.send(embed=embed, file=line)

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.is_timed_out() == False and after.is_timed_out() == True:
            log = [entry async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update)]
            entry = log[0]
            channel = after.guild.get_channel(config["channels"]["punishments_log"])
            line = discord.File("images/line.png")
            embed = discord.Embed(
                title=f"{config["emojis"]["clock"]} Member MUTED",
                description=f"""
                > **User Information**
                > - Ping: <@{after.id}>
                > - Username: `{after.name}`
                
                > **Mute Information**
                > - Staff: <@{entry.user.id}>
                > - Muted until: <t:{int(after.timed_out_until.timestamp())}:F>
                > - Reason: `{entry.reason}`

                Timestamp: <t:{int(time())}:D>
                """,
                color=0xda373c)
            embed.set_thumbnail(url=after.display_avatar.url)
            embed.set_image(url="attachment://line.png")
            await channel.send(embed=embed, file=line)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(punishments_log(client))