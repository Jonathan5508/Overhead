import discord
from discord.ext import commands
import aiohttp

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="help")
    async def helpcmd(self, ctx):
        embed = discord.Embed(title="Help", description="See commands below.", color=discord.Color.embed_background(theme='dark'))
        embed.add_field(
            name="modapps",
            value="`logsetup`\n`modalcreate`\n`appsetup`"
        )
        embed.add_field(
            name="tickets",
            value="`ticketsetup`\n`addrole`\n`removerole`\n`openticket`"
        )
        embed.add_field(
            name="wordverify",
            value="`setpassword`"
        )
        embed.add_field(
            name="misc",
            value="`ping`"
        )
        embed.add_field(
            name="formverify",
            value="`verifyappsetup`\n`createmodal`\n`setupverify`"
        )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))