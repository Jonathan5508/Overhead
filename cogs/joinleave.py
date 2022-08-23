from discord.ext import commands
import discord
from main import coll, apdcoll, vcoll, apucoll

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
        gid = {"_id": guild.id}
        await coll.delete_one(gid)
        await apdcoll.delete_one(gid)
        await vcoll.delete_one(gid)
        await apucoll.delete_one(gid)     

def setup(bot):
    bot.add_cog(joinleave(bot))