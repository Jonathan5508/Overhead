import discord
from discord.ext import commands
from main import apdcoll
from ticketui import TicketSetupView, TicketView

class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketSetupView())
        self.bot.add_view(TicketView())

    ticketcmd = discord.SlashCommandGroup(name="tickets", description="ticket commands")

    @ticketcmd.command(name="ticketsetup", description="sets up ticket channel")
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }
        category = await ctx.guild.create_category(name="tickets", overwrites=overwrites)
        logchannel = await ctx.guild.create_text_channel(name="ticket logs", category=category)
        channel = await ctx.guild.create_text_channel(name="tickets", category=category)
        await apdcoll.update_one({"_id": ctx.guild.id}, {"$set": {"ticketCat": category.id}}, upsert=True)
        await apdcoll.update_one({"_id": ctx.guild.id}, {"$set": {"ticketChannel": channel.id}}, upsert=True)
        await apdcoll.update_one({"_id": ctx.guild.id}, {"$set": {"ticketLogs": logchannel.id}}, upsert=True)
        embed = discord.Embed(title="Open a Ticket!", description="Open a ticket using the button below.")
        await channel.send(embed=embed, view=TicketSetupView())
        await ctx.respond("setup complete!", ephemeral=True)

    @ticketcmd.command(name="addrole", description="Adds a role to ticket handlers.")
    @commands.has_permissions(administrator=True)
    async def add_ticket_role(self, ctx, role:discord.Role):
        data = apdcoll.find({"_id": ctx.guild.id})
        async for channels in data:
            channel = ctx.guild.get_channel(channels["ticketCat"])
        await channel.set_permissions(role, view_channel=True)
        await ctx.respond(f"{role.mention} added to Ticket Channels!")

def setup(bot):
    bot.add_cog(tickets(bot))