import os
import discord 
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

sad_words = ["triste", "depresso", "infeliz", "raiva"]

starter_encouragements = ["Aguenta primo", "As coisas vão melhorar", "Vamos usar calcinha juntos"]

if "responding" not in db.keys():
	db["responding"] = True

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return quote

def update_encouragements(encouraging_message):
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
		encouragements.append(encouraging_message)
		db["encouragements"] = encouragements
	else:
		db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
	encouragements = db["encouragements"]
	if len(encouragements) > index:
		del encouragements[index]
		db["encouragements"] = encouragements

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

	if message.author == client.user:
		return
	
	msg = message.content

	if msg.startswith('$oi'):
		await message.channel.send('Fala meu peixe')

	if message.content.startswith('$inspire'):
		quote = get_quote()
		await message.channel.send(quote)
	
	if db["responding"]:
		options = starter_encouragements
		if "encouragements" in db.keys():
			options = options + db["encouragements"].value

		if any(word in msg for word in sad_words):
			await message.channel.send(random.choice(options))

	if msg.startswith("$new"):
		encouraging_message = msg.split("$new ", 1)[1]
		update_encouragements(encouraging_message)
		await message.channel.send("Nova frase adicionada")
	
	if msg.startswith("$del"):
		encouragements = []
		if "encouragements" in db.keys():
			index = int(msg.split("$del", 1)[1])
			delete_encouragement(index)
			encouragements = db["encouragements"]
		await message.channel.send(encouragements)
	
	if msg.startswith("$list"):
		encouragements = []
		if "encouragements" in db.keys():
			encouragements = db["encouragements"]
		await message.channel.send(encouragements)

	if msg.startswith("$responding"):
		value = msg.split("$responding ", 1)[1]

		if value.lower() == "true":
			db["responding"] = True
			await message.channel.send("Responding is on.")
		else:
			db["responding"] = False
			await message.channel.send("Responding is off.")
	
	if msg.startswith("$xlr8"):
		await message.channel.send(file=discord.File("Images/xlr8.jpg"))

keep_alive()
client.run(os.environ['TOKEN'])