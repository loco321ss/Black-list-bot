import os
import discord

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(client.user)

    guild = client.guilds[0]

    canal = discord.utils.get(guild.voice_channels, name="The Black list")

    await canal.connect()

client.run(TOKEN)
