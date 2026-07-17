import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
CANAL_VOZ = "The Black list"

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    print(f"Cambio de voz: {member.name}")

    canal = discord.utils.get(member.guild.voice_channels, name=CANAL_VOZ)

    if canal is None:
        print("❌ No encontré el canal.")
        return

    personas = [m for m in canal.members if not m.bot]

    print(f"Personas en '{CANAL_VOZ}': {len(personas)}")

    voice_client = member.guild.voice_client

    if len(personas) >= 2:
        if voice_client is None:
            print("Intentando conectar...")
            try:
                await canal.connect()
                print("✅ Conectado al canal.")
            except Exception as e:
                print(f"❌ Error al conectar: {e}")

    else:
        if voice_client is not None:
            print("Desconectando...")
            try:
                await voice_client.disconnect()
                print("👋 Desconectado.")
            except Exception as e:
                print(f"❌ Error al desconectar: {e}")


bot.run(TOKEN)
