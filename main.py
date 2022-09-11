import discord
import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGOSTRING"))

maindb = client.overhead
coll = maindb["applications"]
apdcoll = maindb["appdata"]
vcoll = maindb["verify"]
apucoll = maindb["appusers"]
vdcoll = maindb["vdata"]
vmcoll = maindb["verifymodal"]
vucoll = maindb["vusers"]

intents = discord.Intents
intents.members = True
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

bot.run(os.environ["TOKEN"])