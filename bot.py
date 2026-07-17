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
    print(f"Evento detectado: {member.display_name}")

    canal = discord.utils.get(member.guild.voice_channels, name=CANAL_VOZ)

    if canal is None:
        print("❌ No encontré el canal.")
        return

    personas = [m for m in canal.members if not m.bot]

    print(f"Hay {len(personas)} personas en '{CANAL_VOZ}'")

    voice = member.guild.voice_client

    if len(personas) >= 2:
        if voice is None:
            try:
                print("Intentando entrar...")
                await canal.connect()
                print("✅ Entré al canal.")
            except Exception as e:
                print(f"ERROR: {e}")

    elif len(personas) == 0:
        if voice is not None:
            try:
                print("Saliendo...")
                await voice.disconnect()
                print("✅ Salí del canal.")
            except Exception as e:
                print(f"ERROR: {e}")


bot.run(TOKEN)
