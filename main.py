import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

import random

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '&', 
case_insensitive = True, 
help_command = None,
intents=discord.Intents.all()
)

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

@bot.group(invoke_without_command=True)
async def help(ctx):
  embed = discord.Embed(
    title = "Lista de Comandos",
    description = "Para saber mais sobre um comando, digite  `&help <nome_do_comando>`",
    colour = colour_std
  )
  embed.add_field(name='Geral', value='`ola`, `teste`, `aleatorio`')
  embed.add_field(name='Conselhos', value='`josephEbom`, `cassianoDeuCerto`', inline = False)
  embed.add_field(name='Gerenciar Canais de voz', value='`mv`, `mvAll`, `dct`', inline = False)
  embed.set_footer(text='Todos os comandos não distinguem letras maiúsculas de minúsculas.')
  await ctx.send(embed = embed)

  @help.command()
  async def ola(ctx):
    embed = discord.Embed(
      title = "Ola",
      description = "O bot diz \"Ola!\" a quem lhe cumprimenta.",
      colour = colour_std
    )
    embed.add_field(name = '**Sintaxe**', value = '&ola', inline = False)
    embed.add_field(name = '**Argumentos**', value = 'Este comando não recebe argumentos.')

    await ctx.send(embed = embed)

  @help.command()
  async def teste(ctx):
    embed = discord.Embed(
      title = "Teste",
      description = "O bot retorna uma mensagem de teste para saber se está ativo/online.",
      colour = colour_std
    )
    embed.add_field(name = '**Sintaxe**', value = '&teste', inline = False)
    embed.add_field(name = '**Argumentos**', value = 'Este comando não recebe argumentos.')

    await ctx.send(embed = embed)
  
  @help.command()
  async def aleatorio(ctx):
    embed = discord.Embed(
      title = "Aleatorio",
      description = "O bot escolhe um numero aleatorio no intervalo de dois numeros fornecidos.",
      colour = colour_std
    )
    embed.add_field(name = '**Sintaxe**', value = '&aleatorio n1 n2', inline = False)
    embed.add_field(name = '**Argumentos**', value = 'n1: Primeiro numero do intervalo.\nn2: Segundo numero do intervalo')

    await ctx.send(embed = embed)

  @help.command()
  async def dct(ctx):
    embed = discord.Embed(
      title = "Disconnect",
      description = "Desconecta o usuário especificado do canal de voz onde ele está.",
      colour = colour_std
    )
    embed.add_field(name = '**Sintaxe**', value = '&dct User\n&dct me', inline = False)
    embed.add_field(name = '**Argumentos**', value = 'User: Nome de usuário daquele que será desconectado\nme: Utilizar para desconectar o autor da mensagem.')

    await ctx.send(embed = embed)
  @help.command()
  async def mv(ctx):
    embed = discord.Embed(
      title = "Move",
      description = "Move o usuário especificado para o canal de voz especificado.",
      colour = colour_std
    )
    embed.add_field(name = '**Sintaxe**', value = '&mv User ChannelName\n&mv me ChannelName', inline = False)
    embed.add_field(name = '**Argumentos**', value = 'User: Nome do usuário que será movido\nme: Utilizar para mover o autor da mensagem.\nChannelName: Nome do canal de voz destino.')

    await ctx.send(embed = embed)

#bot diz ola a quem o chama
@bot.command()
async def ola(ctx):
  await ctx.send(f"Ola, {ctx.author.name}")

#teste pra saber se ta ativo
@bot.command()
async def teste(ctx):
  await ctx.send("FALAAAA!")

def get_member(guild : discord.Guild, member_name):
  for vc in guild.voice_channels:
    for member in vc.members:
      if member_name == member.name:
        return member
  raise Exception

def get_channel(guild : discord.Guild, channel_name):
  for vc in guild.voice_channels:
    if channel_name == vc.name:
      return vc
  raise Exception

#para os comandos de mover, o bot deve estar ativo antes dos usuarios entrarem no canal de voz

#Desconecta o usuário do canal de voz onde ele está
@bot.command()
async def dct(ctx, member_name):
  member = None
  embed = None
  if(member_name.upper() == 'ME'):
    try:
      member = get_member(ctx.guild, ctx.author.name)
      embed = criarEmbed(f"@{member.name} pegou o beco.. foi-se embora", colour_std)
    except:
      embed = criarEmbed(f"@{ctx.author.name} nem chegou e já quer sair.", colour_warning)
      await ctx.send(embed = embed)
      return
  else:
    try:
      member = get_member(ctx.guild, member_name)
      embed = criarEmbed(f"@{member.name}, te botaram pra correr!", colour_std)
    except:
      embed = criarEmbed(f"@{member_name} nem chegou e já querem te expulsar.", colour_warning)
      await ctx.send(embed = embed)
      return

  await member.move_to(None)
  await ctx.send(embed = embed)
    

#mover certo membro pra determinado canal
@bot.command()
async def mv(ctx, member_name, channel_name):
  if(member_name.upper() == 'ME'):
    member = get_member(ctx.guild, ctx.author.name)
    try:
      channel = get_channel(ctx.guild, channel_name)
      await member.move_to(channel)
      embed = criarEmbed(f"{ctx.author.name} pegou o beco.. foi parar em {channel_name}", colour_std)
      await ctx.send(embed = embed)
    except:
      embed = criarEmbed(f"Pra onde? Não achei nenhum canal de voz chamado {channel_name}.", colour_warning)
      await ctx.send(embed = embed)
  else:
    try:
      member = get_member(ctx.guild, member_name)
      try:
        channel = get_channel(ctx.guild, channel_name)
        await member.move_to(channel)
        embed = criarEmbed(f"{member_name} pegou o beco.. foi parar em {channel_name}", colour_std)
        await ctx.send(embed = embed)
      except:
        embed = criarEmbed(f"Pra onde? Não achei nenhum canal de voz chamado {channel_name}.", colour_warning)
        await ctx.send(embed = embed)
    except:
      embed = criarEmbed(f"Mover quem? Não vejo {member_name} em nenhum canal de voz.", colour_warning)
      await ctx.send(embed = embed)

#mover todos os membros de um canal para outro
@bot.command()
async def mvAll(ctx, channel_from, channel_to):
  try:
    channel_f = get_channel(ctx.guild, channel_from)
    if len(channel_f.members) == 0:
      embed = criarEmbed(f'Oxente! Pra onde foi a galera que tava em {channel_from}? Não Tem ninguém pra mover...', colour_warning)
      embed.set_thumbnail(url='https://t3.ftcdn.net/jpg/01/09/40/30/240_F_109403011_k3z8NEkKVjBpqOglFuj8Knbea7e4nj5O.jpg')
      await ctx.send(embed = embed)
      return
    try:
      channel_t = get_channel(ctx.guild, channel_to)
      for member in channel_f.members:
        await member.move_to(channel_t)
      embed = criarEmbed(f'Todo mundo do {channel_from} pegou o beco pro {channel_to}.', colour_std)
      embed.set_thumbnail(url='https://cdn-icons.flaticon.com/png/128/1969/premium/1969142.png?token=exp=1636264256~hmac=0616d1e490d6e1adda5d9123534fe99b')
      await ctx.send(embed = embed)
    except:
      embed = criarEmbed(f"Mover pra onde? Não achei nenhum canal de voz chamado {channel_to}.", colour_warning)
      await ctx.send(embed = embed)
  except:
    embed = criarEmbed(f"Mover de onde? Não achei nenhum canal de voz chamado {channel_from}.", colour_warning)
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
async def cassianoDeuCerto(ctx):
  imagens = ["Images/cassiano/so_abalo.png", "Images/cassiano/vdc_n.png", "Images/cassiano/vdc_nao.png", "Images/cassiano/vdc.png"]
  img_escolhida = imagens[random.randint(0, len(imagens) - 1)]
  await ctx.send(file=discord.File(img_escolhida))

@bot.command()
async def josephEbom(ctx):
  imagens = ["Images/joseph/braille.png", "Images/joseph/mexicano.png", "Images/joseph/original.png", "Images/joseph/inverso_moca.png", "Images/joseph/inverso_rapaz.png"]
  img_escolhida = imagens[random.randint(0, len(imagens) - 1)]
  await ctx.send(file=discord.File(img_escolhida))

keep_alive()
bot.run(os.environ['TOKEN'])