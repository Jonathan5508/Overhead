import discord
from discord.ext import commands
from main import vcoll

class WordVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    verifycmd = discord.SlashCommandGroup(name="verify", description="verify commands")

    @verifycmd.command(name="setpassword", description="sets the password and channel.")
    @commands.has_permissions(administrator=True)
    async def setpassword(self, ctx, password, role:discord.Role, channel:discord.TextChannel):
        await vcoll.update_one({"_id": ctx.guild.id}, {"$set": {"password": password}}, upsert=True)
        await vcoll.update_one({"_id": ctx.guild.id}, {"$set": {"role": role.id}}, upsert=True)
        await vcoll.update_one({"_id": ctx.guild.id}, {"$set": {"channel": channel.id}}, upsert=True)
        await ctx.respond("Verify Set!", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        data = vcoll.find({"_id": message.guild.id})
        async for ids in data:
            passw = ids["password"]
            channel = self.bot.get_channel(ids["channel"])
            role = message.guild.get_role(ids["role"])
        if message.content == passw and message.channel == channel:
            await message.author.add_roles(role)
            
def setup(bot):
    bot.add_cog(WordVerify(bot))