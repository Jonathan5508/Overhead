import discord
from main import apdcoll, apucoll
from discord.ui import Modal, InputText, View
import asyncio

class TicketView(View): #class for managing opened tickets
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Close Ticket", row=0, style=discord.ButtonStyle.red, custom_id="close_ticket")

    async def close_btn_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_message("This channel will be deleted shortly.", ephemeral=True)

        data = apdcoll.find({"_id": interaction.guild_id})
        async for ids in data:
            channel = interaction.guild.get_channel(ids["ticketLogs"])
        embed = discord.Embed(title=f"Log Summary for {interaction.user}'s ticket.", description="see below")
        await channel.send(embed=embed)  
        await interaction.channel.delete()

    @discord.ui.button(label="Close With Reason", row=0, style=discord.ButtonStyle.red, custom_id="close_reason")

    async def close_reason(self, button, interaction: discord.Interaction):

        modal = Modal(title="Close Reason")
        modal.add_item(InputText(label="Reason", style=discord.InputTextStyle.short))

        async def modal_callback(interaction: discord.Interaction):
            data = apdcoll.find({"_id": interaction.guild_id})
            async for ids in data:
                channel = interaction.guild.get_channel(ids["ticketLogs"])
            embed = discord.Embed(title=f"Log Summary for {interaction.user}'s ticket.", description="see below")
            embed.add_field(name="Reason", value=modal.children[0].value)
            await interaction.response.send_message("reason submitted!", ephemeral=True)
            await channel.send(embed=embed)
        
        modal.callback = modal_callback
        await interaction.response.send_modal(modal)
        await modal.wait()
        await asyncio.sleep(1)
        await interaction.channel.delete()

class TicketSetupView(View): #class for opening tickets
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="ticket_opener")

    async def btn_callback(self, button, interaction:discord.Interaction):
        username, tag = interaction.user.name, interaction.user.discriminator
        for chn in interaction.guild.channels:
            if username and tag in chn.name:
                return await interaction.response.send_message("You already have an open ticket!", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        data = apdcoll.find({"_id": interaction.guild_id})
        async for ids in data:
            category = interaction.guild.get_channel(ids["ticketCat"])
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True)
        }
        channel = await interaction.guild.create_text_channel(name=f"ticket {interaction.user}", category=category, overwrites=overwrites)
        embed = discord.Embed(title=f"ticket {interaction.user}", description="Describe your issue here.")
        await channel.send(embed=embed, view=TicketView())