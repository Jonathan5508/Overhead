import discord
from discord.ext import commands
from main import apdcoll
from modalcreate import MyModal
from applyui import ApplyView
from appdataui import AppDataView

class ModApps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mappcmd = discord.SlashCommandGroup(name='modapps', description='Command for modapps')

    @mappcmd.command(name="logsetup", description="Set up channels to send apps to")
    @commands.has_permissions(administrator=True)
    async def modappsetup(self, ctx, channel:discord.TextChannel, modrole:discord.Role):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        category = await ctx.guild.create_category(name="modapps", overwrites=overwrites)
        channel = await ctx.guild.create_text_channel(name="modapps", category=category, overwrites=overwrites)
        await apdcoll.update_one({"_id": ctx.guild.id}, {"$set": {"categoryid": category.id}}, upsert=True)
        await apdcoll.update_one({"_id": ctx.guild.id}, {"$set": {"channelid": channel.id}}, upsert=True)
        await apdcoll.update_one({"_id": ctx.guild.id}, {"$set": {"modroleid": modrole.id}}, upsert=True)
        await ctx.respond("Setup Done!", ephemeral=True)

    @mappcmd.command(name="modalcreate", description="creates a mod app modal")
    @commands.has_permissions(administrator=True)
    async def create(self, ctx):
        modal = MyModal(title="Modal Results")
        await ctx.send_modal(modal)

    @mappcmd.command(name="appsetup", description="sets up apps")
    @commands.has_permissions(administrator=True)
    async def appsetup(self, ctx, channel:discord.TextChannel):
        await channel.send("Button Here", view=ApplyView())
        await ctx.respond("ModApps set up!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ApplyView())
        self.bot.add_view(AppDataView())

def setup(bot):
    bot.add_cog(ModApps(bot))