import discord
from discord.ext import commands
from json import load

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import aiohttp

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)


class WelcomeButton(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(emoji="👋", label="Welcome", custom_id="welcome")
    async def welcome_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(f"<@{interaction.user.id}> welcomes <@{self.user.id}>!")
            button.disabled = True
            await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("❌ You can't welcome yourself.", ephemeral=True)


class join_listener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(config["join_role"])
        if role:
            await member.add_roles(role)

        channel = member.guild.get_channel(config["channels"]["chat"])
        background = Image.open("images/templates/welcome.png").convert("RGBA")
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.with_format("png"))) as resp:
                avatar_data = await resp.read()

        avatar = Image.open(BytesIO(avatar_data)).convert("RGBA")
        avatar = avatar.resize((180, 180))

        mask = Image.new("L", avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + avatar.size, fill=255)
        avatar.putalpha(mask)

        background.paste(avatar, (110, 185), avatar)

        draw = ImageDraw.Draw(background)

        font_path = "fonts/ggsans.ttf"

        font1 = ImageFont.truetype(font_path, size=64)
        font2 = ImageFont.truetype(font_path, size=48)

        username = member.name
        draw.text((660, 310), username, font=font1, fill=(255, 255, 255))

        members = str(member.guild.member_count)
        draw.text((877, 435), members, font=font2, fill=(255, 255, 255))

        buffer = BytesIO()
        background.save(buffer, format="PNG")
        buffer.seek(0)

        file = discord.File(fp=buffer, filename="welcome.png")
        await channel.send(f"**Hey** <@{member.id}>", file=file, view=WelcomeButton(member))
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(join_listener(client))