import discord
from discord.ui import View
from main import vdcoll

class VDataView(View): #class for viewing application data
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept-btn")
    async def acc_callback(self, button, interaction: discord.Interaction):
        userid = int(interaction.message.embeds[0].footer.text)
        userobj = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
        username = userobj.name
        data2 = await vdcoll.find_one({"_id": interaction.guild_id})
        role = interaction.guild.get_role(data2["verifyroleid"])
        await userobj.add_roles(role)

        await userobj.send("You have been verified, welcome!")
        await vdcoll.update_one({"_id": interaction.guild_id}, {"$unset": {username: userid}})
        await interaction.message.delete(delay=2)