import discord 
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()

bot = commands.Bot(command_prefix = '&', case_insensitive = True)

#avisar no console que o bot ta on
@bot.event
async def on_ready():
  print("{0.user.name} tá on!".format(bot))

#bot diz ola a quem o chama
@bot.command()
async def ola(ctx):
  await ctx.send(f"Ola, {ctx.author.name}")

#teste pra saber se ta ativo
@bot.command()
async def teste(ctx):
  await ctx.send("FALAAAA!")

#mover certo membro pra determinado canal
@bot.command()
async def move(ctx, member : discord.Member, channel : discord.VoiceChannel):
  await member.move_to(channel)

#mover todos os membros de um canal para outro
#o bot deve estar ativo antes dos usuarios entrarem no canal de voz e tentarem mudar
@bot.command()
async def move_all(ctx, channel_from : discord.VoiceChannel, channel_to : discord.VoiceChannel):
  for member in channel_from.members:
    await member.move_to(channel_to)

#escolher numero aleatorio entre dois numeros fornecidos
@bot.command()
async def aleatorio(ctx, numero1, numero2):
  n = random.randint(int(numero1), int(numero2))
  await ctx.send(f"O numero aletório escolhido entre {numero1} e {numero2} foi {n}.")

@bot.command()
async def josephEbom(ctx):
  imagens = ["Images/braille.png", "Images/mexicano.png", "Images/original.png", "Images/inverso_moca.png"]
  img_escolhida = imagens[random.randint(0, len(imagens))]
  await ctx.send(file=discord.File(img_escolhida))


bot.run(os.environ['TOKEN'])

#client.run(DISCORD_TOKEN)