import discord
import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')
mongostr = os.getenv('MONGO_STRING')
client = motor.motor_asyncio.AsyncIOMotorClient(mongostr)

maindb = client.overhead
coll = maindb["applications"]
apdcoll = maindb["appdata"]
vcoll = maindb["verify"]
apucoll = maindb["appusers"]

intents = discord.Intents.all()
bot = discord.Bot(intents=intents, help_command=None)

for files in os.listdir("./cogs"):
    if files.endswith(".py"):
        cogf = files[:-3]
        try:
            bot.load_extension(f"cogs.{cogf}")
            print(f"{cogf} initialized!")
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.slash_command(name="ping", description="Pong")
async def ping(ctx):
    await ctx.respond(f"Pong! {round(bot.latency) * 1000}")

bot.run(token)