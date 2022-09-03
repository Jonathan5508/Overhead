import discord
from discord.ext import commands
from discord.ui import View, Modal, InputText
from main import vmcoll, vdcoll, vucoll
from uiutils import vdataui

class VDataSetup(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Verify", custom_id="verify-btn", style=discord.ButtonStyle.green)
    async def verify_callback(self, button, interaction: discord.Interaction):
        data = vmcoll.find({"_id": interaction.guild_id})
        modal = Modal(title="Mod App")
        async for field in data:
            for keys in field.keys():
                if keys == "_id":
                    continue
                if keys == "Verify 1":
                    modal.add_item(InputText(label=field[keys]))
                    continue
                modal.add_item(InputText(label=field[keys], style=discord.InputTextStyle.long))

        async def modal_callback(interaction: discord.Interaction):
            try:
                descstr = ""
                data = vdcoll.find({"_id": interaction.guild_id})
                fielddata = vmcoll.find({"_id": interaction.guild_id})
                i = 0
                async for fields in fielddata:
                    for keys in fields.keys():
                        if keys == "_id":
                            continue
                        q = fields[keys]
                        descstr += f"**{q}**\n{modal.children[i].value}\n\n"
                        i += 1
                async for ids in data:
                    channel = interaction.guild.get_channel(ids['channelid'])
                vucoll.update_one({"_id": interaction.guild_id}, {"$set": {interaction.user.name: interaction.user.id}}, upsert=True)
                embed = discord.Embed(title="App Results", description=descstr)
                embed.set_footer(text=interaction.user.id)
                await channel.send(embed=embed, view=vdataui.VDataView())
                await interaction.response.send_message("App sent!", ephemeral=True)
            except KeyError:
                await interaction.response.send_message("The mod apps have not completed setup!")
            except discord.HTTPException:
                await interaction.response.send_message("An error occurred while submitting the app, likely due to a field being too long.")

        modal.callback = modal_callback
        await interaction.response.send_modal(modal)