import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  username = str(message.author).split('#')[0]
  user_message = str(message.content)
  channel = str(message.channel.name)
  print(f'{username}: {user_message} ({channel}')
  
  if message.author == client.user:
    return

  if message.channel.name == 'general':
    if user_message.lower() == 'hello':
      await message.channel.send(f'Hello {username}!')
      return
    elif user_message.lower() == 'bye':
      await message.channel.send(f'See you later {username}!')
      return
    elif user_message.lower() == 'วันนี้ทำอะไร':
      await message.channel.send(f'นอนเล่น {username}!')
      return
    elif user_message.lower() == 'ขายกล่องละเท่าไหร่':
      await message.channel.send(f'กล้อยปิ้งมะพร้าวอ่อน กล่องละ 25 บ. จ้าคุณ {username}!')
      return
    elif user_message.lower() == 'โจก':
      await message.channel.send(f'ควย {username}!')
      return
    elif user_message.lower() == 'i make you alive':
      await message.channel.send(f'Thank you for giving me life, I appreciate you {username}!')
      return
    elif user_message.lower() == 'what is your favorite food':
      await message.channel.send(f'Pad Ka Pa: Stir Fried Basil {username}!')
      return
    elif user_message.lower() == 'do you know my girlfriend?':
      await message.channel.send(f' Her name is KIK  {username}!')
      return

    elif user_message.lower() == '!random':
      response = f'This is your number: {random.randrange(1000000)}'
      await message.channel.send(response)
      return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))
