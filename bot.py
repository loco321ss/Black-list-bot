import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
CANAL_VOZ = "The Black list"

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Evita que connect() se ejecute varias veces al mismo tiempo
conectando = False


@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    global conectando

    canal = discord.utils.get(member.guild.voice_channels, name=CANAL_VOZ)

    if canal is None:
        return

    personas = [m for m in canal.members if not m.bot]
    cantidad = len(personas)

    print(f"{cantidad} personas en '{CANAL_VOZ}'")

    voice = member.guild.voice_client

    # Si hay 2 o más personas
    if cantidad >= 2:

        # Ya está conectado
        if voice and voice.is_connected():
            print("Ya estoy conectado.")
            return

        # Ya hay un intento de conexión en curso
        if conectando:
            print("Ya estoy intentando conectar...")
            return

        conectando = True

        try:
            print("Entrando al canal...")
            await canal.connect(timeout=30, reconnect=True)
            print("✅ Conectado.")
        except Exception as e:
            print("ERROR:", e)
        finally:
            conectando = False

    # Si queda 1 o ninguna persona, salir
    else:
        if voice and voice.is_connected():
            try:
                print("Saliendo del canal...")
                await voice.disconnect(force=True)
                print("✅ Desconectado.")
            except Exception as e:
                print("ERROR:", e)
