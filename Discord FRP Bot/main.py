import discord
from discord.ext import commands
from utils import *
from function import *
import os

Intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix="-", intents=Intents)
game = Game()


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name="Kumar"))
    print("Hazırım Abisu :)")


@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="gidenler")
    await channel.send(f"{member} sie!")
    print(f"{member} sie!")


@Bot.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount + 1)


@Bot.command()
async def load(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        Bot.load_extension(f'cogs.{extension}')
        await ctx.send('Yüklendi!')


@Bot.command()
async def unload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        Bot.unload_extension(f'cogs.{extension}')
        await ctx.send('Kaldırıldı!')


@Bot.command(pass_context=True)
async def reload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        Bot.unload_extension(f'cogs.{extension}')
        Bot.load_extension(f'cogs.{extension}')
        await ctx.send('Geri Yüklendi!')


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        Bot.load_extension(f'cogs.{filename[:-3]}')

Bot.run(Token)
