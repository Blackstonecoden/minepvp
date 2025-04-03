import discord
from discord.ext import commands
from json import load
import random

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

class temp_channel_listener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.temp_channels = {}

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        category = self.client.get_channel(config["categories"]["temp_channels"])
        if category is not None and isinstance(category, discord.CategoryChannel):
            for channel in category.voice_channels:
                if channel.id != config["channels"]["temp_join"]:
                    await channel.delete()

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None and after.channel != before.channel:
            if after.channel.id == config["channels"]["temp_join"]:
                category = self.client.get_channel(config["categories"]["temp_channels"])

                overwrites = {}
                overwrites[member.guild.default_role] = discord.PermissionOverwrite(send_messages=False)
       
                temp_channel = await category.create_voice_channel(name=f"🔊〡{member.name}", overwrites=overwrites)    
                await member.move_to(temp_channel)
                self.client.temp_channels[str(temp_channel.id)] = {"channel_owner": member.id}

        if before.channel is not None and after.channel != before.channel:
            try:
                channel_id = before.channel.id
                if str(channel_id) in self.client.temp_channels:
                    if self.client.temp_channels[str(channel_id)]["channel_owner"] == member.id:
                        if len(before.channel.members) == 0:
                            await before.channel.delete()
                            del self.client.temp_channels[str(channel_id)]
                        else:
                            random_member = random.choice(before.channel.members)
                            self.client.temp_channels[str(channel_id)]["channel_owner"] = random_member.id


            except:
                return
            
async def setup(client:commands.Bot) -> None:
    await client.add_cog(temp_channel_listener(client))