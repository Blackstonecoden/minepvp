import discord
from discord.ext import commands
from json import load

from datetime import timedelta
import re

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)

TIME_UNITS = {
    "s": ("Second", timedelta(seconds=1)),
    "m": ("Minute", timedelta(minutes=1)),
    "h": ("Hour", timedelta(hours=1)),
    "d": ("Day", timedelta(days=1))
}

def parse_duration(duration: str):
    match = re.fullmatch(r"(\d+)\s*([smhd])", duration.strip().lower())
    if not match:
        return None, None
    amount, unit = int(match[1]), match[2]
    return amount * TIME_UNITS[unit][1], (amount, TIME_UNITS[unit][0])


class MuteTextCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
     
    @commands.command(name="mute")
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, duration: str, *, reason: str = "No reason provided"):
        time, (amount, unit_name) = parse_duration(duration)
        if not time:
            return await ctx.reply("❌ Invalid duration format. Use formats like `1m`, `1h`, `1d`.", mention_author=False)
        
        await member.timeout(time, reason=reason)
        plural = "s" if amount != 1 else ""
        await ctx.reply(f"{member.mention} has been muted for **{amount} {unit_name}{plural}**. Reason: `{reason}`.", mention_author=False, allowed_mentions=discord.AllowedMentions(users=False))

    @mute.error
    async def mute_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            msg = "❌ You're missing the required permissions for that command."
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = "❌ Missing argument: `?mute <member> <duration> [reason]`."
        elif isinstance(error, commands.BadArgument):
            msg = "❌ Couldn't parse one or more arguments."
        else:
            msg = "❌ An unexpected error occurred."
            raise error
        await ctx.reply(msg, mention_author=False)

async def setup(client: commands.Bot):
    await client.add_cog(MuteTextCommand(client))