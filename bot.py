import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

CANAL_VOZ = "The Black list"

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

conectado = False


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    global conectado

    if member.bot:
        return

    canal = discord.utils.get(member.guild.voice_channels, name=CANAL_VOZ)

    if canal is None:
        return

    personas = [m for m in canal.members if not m.bot]

    if len(personas) >= 1 and not conectado:
        await canal.connect()
        conectado = True
        print("Entré al canal")

    elif len(personas) < 1 and conectado:
        if canal.guild.voice_client:
            await canal.guild.voice_client.disconnect()
        conectado = False
        print("Salí del canal")


bot.run(TOKEN)
