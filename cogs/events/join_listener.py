import discord
from discord.ext import commands
from json import load

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class join_listener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(config["join_role"])
        if role:
            await member.add_roles(role)
            

async def setup(client:commands.Bot) -> None:
    await client.add_cog(join_listener(client))