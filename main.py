import os
import discord 
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '%', case_insensitive = True)

@client.event
async def on_ready():
  print("Entramos com {0.user}".format(client))

@client.command()
async def ola(ctx):
  await ctx.send(f"Olá, {ctx.author}")

@client.command()
async def aleatorio(ctx, numero1, numero2):
  n = random.randint(int(numero1), int(numero2))
  await ctx.send(f"O numero aletório escolhido entre {numero1} e {numero2} foi {n}.")

client.run(os.environ['TOKEN'])
