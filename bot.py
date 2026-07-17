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
    print(f"✅ Bot conectado como {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):
    # Ignorar otros bots
    if member.bot:
        return

    # Buscar el canal de voz
    canal = discord.utils.get(member.guild.voice_channels, name=CANAL_VOZ)

    if canal is None:
        return

    # Contar únicamente personas (sin bots)
    personas = [m for m in canal.members if not m.bot]

    voice_client = member.guild.voice_client

    # Entrar cuando haya 2 o más personas
    if len(personas) >= 2:
        if voice_client is None:
            try:
                await canal.connect()
                print("✅ Entré al canal.")
            except Exception as e:
                print(f"❌ Error al conectar: {e}")

    # Salir cuando quede menos de 2 personas
    else:
        if voice_client is not None:
            try:
                await voice_client.disconnect()
                print("👋 Salí del canal.")
            except Exception as e:
                print(f"❌ Error al desconectar: {e}")


bot.run(TOKEN)
