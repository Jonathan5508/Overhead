import discord
from discord.ui import View, Modal, InputText
from main import apdcoll, apucoll, coll
from uiutils import appdataui

class ApplyView(View): #class for applying
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Apply", custom_id="apply-button", style=discord.ButtonStyle.green)
    async def btn_callback(self, button, interaction: discord.Interaction):
        data = coll.find({"_id": interaction.guild_id})
        modal = Modal(title="Mod App")
        async for field in data:
            for keys in field.keys():
                if keys == "_id":
                    continue
                if keys == "Field 1":
                    modal.add_item(InputText(label=field[keys]))
                    continue
                modal.add_item(InputText(label=field[keys], style=discord.InputTextStyle.long))

        async def modal_callback(interaction: discord.Interaction):
            try:
                descstr = ""
                data = apdcoll.find({"_id": interaction.guild_id})
                fielddata = coll.find({"_id": interaction.guild_id})
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
                apucoll.update_one({"_id": interaction.guild_id}, {"$set": {interaction.user.name: interaction.user.id}}, upsert=True)
                embed = discord.Embed(title="App Results", description=descstr)
                embed.set_footer(text=interaction.user.id)
                await channel.send(embed=embed, view=appdataui.AppDataView())
                await interaction.response.send_message("App sent!", ephemeral=True)
            except KeyError:
                await interaction.response.send_message("The mod apps have not completed setup!")
            except discord.HTTPException:
                await interaction.response.send_message("An error occurred while submitting the app, likely due to a field being too long.")

        modal.callback = modal_callback
        await interaction.response.send_modal(modal)