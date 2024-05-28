# Main file, run the file to start the bot
import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN
from strava import get_lunch

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="hey", description="Say hey to the bot, he might reply back!")
async def hey(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")

@bot.tree.command(name="lunch", description="Get the lunch menu for the current week")
async def lunch(interaction: discord.Interaction):
    await interaction.response.send_message(get_lunch(), ephemeral=True)

bot.run(TOKEN)