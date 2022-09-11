import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_appliction_command_error(self, ctx, error):
        embed = discord.Embed(title="Error", description=error, color=discord.Color.embed_background(theme="dark"))
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))