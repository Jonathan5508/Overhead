import discord
from discord.ui import Modal, InputText
from main import coll, vmcoll

class MyModal(Modal): #class to set up app modal
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Field 1", placeholder="1st field, recommended for username"))
        self.add_item(InputText(label="Field 2", placeholder="2nd field, 1st question (max 45 chars)", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Field 3", placeholder="3rd field, 2nd question (max 45 chars)", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Field 4", placeholder="4th field, 3rd question (max 45 chars)", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Input Boxes")
        i = 1
        for values in self.children:
            await coll.update_one({"_id": interaction.guild_id}, {"$set": {f"Field {i}": values.value}}, upsert=True)
            embed.add_field(name=f"Field {i}", value=values.value)
            i += 1
        await interaction.response.send_message("Modal Set up!", ephemeral=True)

class VerifyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Verify 1", placeholder="1st field, recommended for username"))
        self.add_item(InputText(label="Verify 2", placeholder="2nd field, 1st question (max 45 chars)", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Verify 3", placeholder="3rd field, 2nd question (max 45 chars)", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Verify 4", placeholder="4th field, 3rd question (max 45 chars)", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Input Boxes")
        i = 1
        for values in self.children:
            await vmcoll.update_one({"_id": interaction.guild_id}, {"$set": {f"Verify {i}": values.value}}, upsert=True)
            embed.add_field(name=f"Verify {i}", value=values.value)
            i += 1
        await interaction.response.send_message("Modal Set up!", ephemeral=True)