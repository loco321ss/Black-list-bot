import os
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("TOKEN")
CANAL_VOZ = "The Black list"

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")

    if not revisar_canal.is_running():
        revisar_canal.start()


@tasks.loop(minutes=5)
async def revisar_canal():
    print("Revisando canal...")

    for guild in bot.guilds:

        canal = discord.utils.get(guild.voice_channels, name=CANAL_VOZ)

        if canal is None:
            continue

        personas = [m for m in canal.members if not m.bot]

        print(f"Hay {len(personas)} personas.")

        voice = guild.voice_client

        if len(personas) >= 2:

            if voice is None or not voice.is_connected():
                try:
                    print("Entrando...")
                    await canal.connect(timeout=30)
                    print("✅ Conectado.")
                except Exception as e:
                    print(e)

        else:

            if voice and voice.is_connected():
                try:
                    print("Saliendo...")
                    await voice.disconnect(force=True)
                    print("✅ Desconectado.")
                except Exception as e:
                    print(e)


bot.run(TOKEN)
