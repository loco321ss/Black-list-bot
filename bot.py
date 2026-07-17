import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

CANAL_VOZ = "The Black list"

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    canal = discord.utils.get(member.guild.voice_channels, name=CANAL_VOZ)

    if canal is None:
        print("No encontré el canal de voz")
        return

    personas = [m for m in canal.members if not m.bot]

    if len(personas) >= 2:
        if canal.guild.voice_client is None:
            await canal.connect()
            print("Entré al canal")

    elif len(personas) < 2:
        if canal.guild.voice_client:
            await canal.guild.voice_client.disconnect()
            print("Salí del canal")


bot.run(TOKEN)
