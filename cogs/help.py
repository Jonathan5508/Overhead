import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="help")
    async def helpcmd(self, ctx):
        embed = discord.Embed(title="Help", description="See commands below.")
        embed.add_field(
            name="modapps",
            value="`logsteup`\n`modalcreate`\n`appsetup`"
        )
        embed.add_field(
            name="tickets",
            value="`ticketset`\n`addrole`"
        )
        embed.add_field(
            name="wordverify",
            value="`setpassword`"
        )
        embed.add_field(
            name="misc",
            value="`ping`"
        )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))