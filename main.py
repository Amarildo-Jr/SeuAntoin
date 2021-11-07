import os
import discord
from discord.ext import commands

import random

bot = commands.Bot(command_prefix = '&', case_insensitive = True, help_command = None)

colour_std = 16744576
colour_warning = 16777028

def criarEmbed(title, colour):
  embed = discord.Embed(
    title = title,
    colour = colour
  )
  return embed

def criarEmbedThumb(title, colour, image):
  embed = discord.Embed(
    title = title,
    colour = colour
  )
  return embed


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
  try:
    await member.move_to(channel)
  except:
    print('Alooooooooo')
    await ctx.send('Mover quem? Pra onde?')

#mover todos os membros de um canal para outro
#o bot deve estar ativo antes dos usuarios entrarem no canal de voz e tentarem mudar
@bot.command()
async def move_all(ctx, channel_from : discord.VoiceChannel, channel_to : discord.VoiceChannel):
  x = len(channel_from.members) == 0
  if x:
    embed = criarEmbed(f'Oxente! Pra onde foi a galera que tava em {channel_from.name}? Não Tem ninguém pra mover...', colour_warning)
    embed.set_thumbnail(url='https://t3.ftcdn.net/jpg/01/09/40/30/240_F_109403011_k3z8NEkKVjBpqOglFuj8Knbea7e4nj5O.jpg')
    await ctx.send(embed = embed)
    return
  else:
    for member in channel_from.members:
      await member.move_to(channel_to)
          
  embed = criarEmbed(f'Todo mundo do {channel_from.name} pegou o beco pro {channel_to.name}.', colour_std)
  embed.set_thumbnail(url='https://cdn-icons.flaticon.com/png/128/1969/premium/1969142.png?token=exp=1636264256~hmac=0616d1e490d6e1adda5d9123534fe99b')
  await ctx.send(embed = embed)

#escolher numero aleatorio entre dois numeros fornecidos
@bot.command()
async def aleatorio(ctx, numero1, numero2):
  text = ''
  if numero1 > numero2:
    [numero1, numero2] = [numero2, numero1]
  n = random.randint(int(numero1), int(numero2))
  if(numero1 < numero2):
    text = f"O numero aletório escolhido entre {numero1} e {numero2} foi {n}."
  elif numero1 == numero2:
    text = f"Falar pra você que estou surpreso! Aleatoriamente, entre {numero1} e {numero2} foi escolhido o {n}."
  embed = criarEmbed(text, colour_std)
  embed.set_thumbnail(url='https://4.bp.blogspot.com/-fTbckS3pcCE/VzUTUdqpM7I/AAAAAAAAUmY/WXLhewpgNIUhzqvEf7zrCItUGpif3e4GQCLcB/s1600/Gifs%2Banimados%2BDado%2B8.gif')
  await ctx.send(embed = embed)

@bot.command()
async def josephEbom(ctx):
  imagens = ["Images/braille.png", "Images/mexicano.png", "Images/original.png", "Images/inverso_moca.png", "Images/inverso_rapaz.png"]
  img_escolhida = imagens[random.randint(0, len(imagens) - 1)]
  await ctx.send(file=discord.File(img_escolhida))

bot.run(os.environ['TOKEN'])