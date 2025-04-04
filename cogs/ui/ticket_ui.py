import discord
from discord.ext import commands
from json import load, dump
import time

with open("config.json", 'r', encoding='utf-8') as file:
    config = load(file)
with open("data/ticket_list.json", 'r') as file:
    tickets = load(file)

ticket_types = [
    discord.SelectOption(
        label=ticket["name"],
        description=ticket["description"],
        emoji=config["emojis"][ticket["discord_emoji"]],
        value=key
    )
    for key, ticket in config["ticket_types"].items()
]


class TicketMenu(discord.ui.Select):
    def __init__(self, client:commands.Bot):
        super().__init__(placeholder="Select an option", options=ticket_types, custom_id="ticket_options")
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        self.view.clear_items()
        self.view.add_item(TicketMenu(self.client))
        await interaction.message.edit(view=self.view)
        
        value = self.values[0]
        if config["ticket_types"][value]["disabled"] == True:
            await interaction.response.send_message(f"❌ Currently not available.", ephemeral=True)
            return

        for ticket in self.client.ticket_list.values():
            if ticket["ticket_owner"] == str(interaction.user.id):
                await interaction.response.send_message(f"❌ You already have an open ticket.", ephemeral=True)
                return
            
        category = self.client.get_channel(config["categories"]["tickets"])
        ticket_channel = await category.create_text_channel(name=f"{config["ticket_types"][value]["emoji"]}｜{interaction.user.name}")
        
        line = discord.File("images/line.png")
        embed = discord.Embed(
            description=f"""
            ## Ticket Successfully Created

            You've successfully created a ticket with the reason `{config["ticket_types"][value]["short_name"]}`.
            Go to the channel <#{ticket_channel.id}> to start your conversation with the team.
            """,
            color=0x248046)
        embed.set_image(url="attachment://line.png")
        await interaction.response.send_message(embed=embed, files=[line], ephemeral=True)


        await ticket_channel.set_permissions(ticket_channel.guild.default_role,read_messages=False, send_messages=False)
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        for role_id in config["ticket_types"][value]["roles"]:
            role = interaction.guild.get_role(role_id)
            if role:
                await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

        line = discord.File("images/line.png")
        embed = discord.Embed(
            title=f"{config["emojis"]["mail"]} TICKET",
            description=f"""
            > **Ticket Information**
            > - User: {interaction.user.mention}
            > - Reason: `{config["ticket_types"][value]["short_name"]}`
            > - Created: <t:{int(time.time())}:R> 
            
            > **Information for the user**
            > - Please describe your issue as clearly as possible so the team can help you quickly.
            > - Please be patient until the team gets back to you.
            """,
            color=0x56565d)
        embed.set_image(url="attachment://line.png")
        message = await ticket_channel.send(embed=embed, files=[line], view=TicketButtons(self.client))
        await message.pin()

        self.client.ticket_list[str(ticket_channel.id)] = {"ticket_owner": str(interaction.user.id),"created_at": int(time.time()), "ticket_type": value}
        with open("data/ticket_list.json", 'w') as file:
            dump(self.client.ticket_list, file, indent=4)


class TicketMenuView(discord.ui.View):
    def __init__(self, client:commands.Bot):
        super().__init__(timeout=None)
        self.add_item(TicketMenu(client))


class TicketButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=config["emojis"]["user_plus"], custom_id="add_user_ticket", row=0)
    async def add_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == int(self.client.ticket_list[str(interaction.channel.id)]["ticket_owner"]) or any(role.id in config["ticket_types"][self.client.ticket_list[str(interaction.channel.id)]["ticket_type"]]["roles"] for role in interaction.user.roles) == True:
            line = discord.File("images/line.png")
            embed = discord.Embed(
                description=f"""
                ## Add User
                Select the user below that you want to add to this ticket so they can help you.
                """,
                color=0x56565d)
            embed.set_image(url="attachment://line.png")
            view = AddUserView(self.client, interaction.channel.id)
            await interaction.response.send_message(embed=embed, files=[line], view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ You are not the creator of this ticket.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["user_minus"], custom_id="remove_user_ticket", row=0)
    async def remove_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == int(self.client.ticket_list[str(interaction.channel.id)]["ticket_owner"]) or any(role.id in config["ticket_types"][self.client.ticket_list[str(interaction.channel.id)]["ticket_type"]]["roles"] for role in interaction.user.roles) == True:
            line = discord.File("images/line.png")
            embed = discord.Embed(
                description=f"""
                ## Remove User
                Select the user below that you want to remove from this ticket, for example if you no longer need them.
                """,
                color=0x56565d)
            embed.set_image(url="attachment://line.png")
            view = RemoveUserView(self.client, interaction.channel.id)
            await interaction.response.send_message(embed=embed, files=[line], view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ You are not the creator of this ticket.", ephemeral=True)

    @discord.ui.button(emoji=config["emojis"]["trash_red"], custom_id="close_ticket", row=0)
    async def close_ticket_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if  any(role.id in config["ticket_types"][self.client.ticket_list[str(interaction.channel.id)]["ticket_type"]]["roles"] for role in interaction.user.roles) == True:
            line = discord.File("images/line.png")
            embed = discord.Embed(
                description=f"""
                ## Close Ticket
                Are you sure you want to close this ticket? Click the red button below if you want to close it.
                """,
                color=0xda373c)
            embed.set_image(url="attachment://line.png")
            view = CloseConfirmButtons(self.client)
            await interaction.response.send_message(embed=embed, files=[line], view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ You are not ticket staff.", ephemeral=True)


class CloseConfirmButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=15)
        self.client = client
        self.message = None

    @discord.ui.button(emoji=config["emojis"]["trash"], style=discord.ButtonStyle.red, row=0)
    async def lock_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.delete()

        if str(interaction.channel.id) in self.client.ticket_list:
            del self.client.ticket_list[str(interaction.channel.id)]
            with open("data/ticket_list.json", 'w') as file:
                dump(self.client.ticket_list, file, indent=4)
        else:
            return

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            return


class AddUserMenu(discord.ui.UserSelect):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(placeholder="Select an option")
        self.client = client
        self.channel_id = channel

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].id == interaction.user.id:
            await interaction.response.send_message("❌ You can't add yourself.", ephemeral=True)
            return
        channel = self.client.get_channel(self.channel_id)
        member = channel.guild.get_member(self.values[0].id)
        if member.bot:
            await interaction.response.send_message("❌ You can't add APPs.", ephemeral=True)
            return
        
        await interaction.response.send_message("✅ User addes successfully.", ephemeral=True)
        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = True
        overwrite.send_messages = True
        await channel.set_permissions(member, overwrite=overwrite)


class AddUserView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(AddUserMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, AddUserMenu):
                child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                return


class RemoveUserMenu(discord.ui.UserSelect):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(placeholder="Select an option")
        self.client = client
        self.channel_id = channel

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].id == interaction.user.id:
            await interaction.response.send_message("❌ You can't remove yourself.", ephemeral=True)
            return
        channel = self.client.get_channel(self.channel_id)
        member = channel.guild.get_member(self.values[0].id)
        if member.bot:
            await interaction.response.send_message("❌ You can't remove APPs.", ephemeral=True)
            return
        await interaction.response.send_message("✅ User removed successfully.", ephemeral=True)
        await channel.set_permissions(member, overwrite=None)


class RemoveUserView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(RemoveUserMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, RemoveUserMenu):
                child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                return


class ticket_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.ticket_list = tickets

async def setup(client:commands.Bot) -> None:
    await client.add_cog(ticket_system(client))