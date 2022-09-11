from discord.ext import commands
import discord
from main import coll, apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll

class joinleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        user = self.bot.user
        embed = discord.Embed(title="Thanks For Inviting Me!", description="Type /help for more information.")
        embed.set_thumbnail(url=user.avatar.url)
        for channel in guild.channels:
            try:
                await channel.send(embed=embed)
                return
            except:
                continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        ls = [apdcoll, vcoll, apucoll, vdcoll, vmcoll, vucoll, coll]
        gid = {"_id": guild.id}
        for colls in ls:
            await colls.delete_one(gid)  

def setup(bot):
    bot.add_cog(joinleave(bot))