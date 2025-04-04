import discord
from discord.ext import commands


class pin_message_listener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.last_activities = {}

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.id != self.client.user.id:
            return
        
        if message.type == discord.MessageType.pins_add:
            await message.delete()

async def setup(client:commands.Bot) -> None:
    await client.add_cog(pin_message_listener(client))