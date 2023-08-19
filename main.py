import discord
from discord.ext import commands

#use your own token
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def setup_hook():
    await bot.load_extension("sub")


bot.run(token=TOKEN)
