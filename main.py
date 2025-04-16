import discord
from discord.ext import commands
import os
from keep_alive import keep_alive  # mantém o bot online 24h

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs dos canais
CANAL_ORIGEM = 1234567890  # Substitua pelos seus
CANAL_APROVADO = 1234567890
CANAL_NEGADO = 1234567890

@bot.event
async def on_ready():
    print(f"🤖 Bot está online como {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != CANAL_ORIGEM:
        return

    guild = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)

    content = message.content
    author = message.author.display_name
    revisor = user.display_name

    if str(payload.emoji.name) == "✅":
        destino = guild.get_channel(CANAL_APROVADO)
        await destino.send(f"✅ **Conteúdo aprovado!**\n\n📄 {content}\n🧑‍💻 Autor: {author}\n🔍 Aprovado por: {revisor}")
    elif str(payload.emoji.name) == "❌":
        destino = guild.get_channel(CANAL_NEGADO)
        await destino.send(f"❌ **Conteúdo reprovado!**\n\n📄 {content}\n🧑‍💻 Autor: {author}\n🛑 Reprovado por: {revisor}")

# manter online
keep_alive()
bot.run(os.environ['TOKEN'])
