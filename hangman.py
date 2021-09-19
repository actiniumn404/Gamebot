import discord
import random
import requests
import json
import string

hangmangames = {}
hangstages = [
"""
+ - |
|   
|   
|  
|______
""",
"""
+ - |
|   O
|   
|  
|______
""",
  """
+ - |
|   O
|   |
|  
|______
""",
"""
+ - |
|   O
|  \|
|  
|______
""",
"""
+ - |
|   O
|  \|/
|  
|______
""",
"""
+ - |
|   O
|  \|/
|  / 
|______
""",
"""
+ - |
|   O
|  \|/
|  / \\
|______
"""
]

async def new(message, newhangman):
  await message.delete()
  while True:
    id = random.randint(10000, 99999)
    if id not in list(hangmangames.keys()):
      break

  query = str(newhangman.group(1)).lower()
  if query == "*":
    query = json.loads(requests.get('https://random-word-api.herokuapp.com/word').text)[0]

  hangmangames[id] = [query.lower(), str(message.author), [" "], 0]
  hashed = ""
  for x in list(query):
    if x == " ":
      hashed += " "
    else:
      hashed += "#"
  
  embed = discord.Embed(
    title="New Hangman game",
    color=discord.Color.from_rgb(252, 164, 28)
  )
  embed.set_author(name=f"Gamebot")
  if all([x.lower() in string.ascii_lowercase+" " for x in list(query)]):
    embed.add_field(name="New game", value=f"{str(message.author)} has created hangman game number {id}!", inline=False)
    embed.add_field(name="The Pattern", value=f"`{hashed}`", inline=False)
    embed.add_field(name="How to guess", value=f"To guess a letter, type `!hangman {str(id)} guess LETTER`. More info at the documentation (gamebot!help)", inline=False)
  else:
    embed.add_field(name="ERROR", value=f"`ONLY LETTERS IN QUERY PLEASE`", inline=False)
  embed.set_footer(text=f"For all gamebot commands, type gamebot!help")

  await message.channel.send(embed=embed)


async def guess(message, hangmanguess):
  embed = discord.Embed(
    title="Hangman guess",
    color=discord.Color.from_rgb(252, 164, 28)
  )
  embed.set_author(name=f"Gamebot")
  embed.set_footer(text=f"For all gamebot commands, type gamebot!help")

  id = int(hangmanguess.group(1))
  if id in list(hangmangames.keys()):
    letter = hangmanguess.group(2).lower()
    pattern = hangmangames[id][0]
    guessed = hangmangames[id][2]
    if letter not in guessed:
      hashed = ""
      if letter not in pattern:
        hangmangames[id][3] += 1

      else:
        hangmangames[id][2].append(letter)

      for x in list(pattern):
        if x in guessed:
          hashed += x
        else:
          hashed += "#"

      if "#" in hashed:
        embed.add_field(name="Current pattern", value=f"```{hashed}```", inline=False)
        embed.add_field(name="Current hangstage", value=f"```{hangstages[hangmangames[id][3] if not hangmangames[id][3] >= 6 else 6]}```", inline=True)
      if hangmangames[id][3] >= 6:
        embed.add_field(name="Game over", value=f"Whoops, you failed. The pattern was `{pattern}`. This game will be deleted", inline=False)
        hangmangames.pop(id)
      if not "#" in hashed and not hangmangames[id][3] >= 7:
        embed.add_field(name="Game over", value=f"Congragulations! You guessed the phrase, which was `{pattern}`, with only {str(7-hangmangames[id][3])} 'hangs' left! This game will be deleted", inline=False)
        hangmangames.pop(id)
    else:
      embed.add_field(name="ERROR", value=f"```ERROR: {letter} HAS ALREADY BEEN GUESSED```", inline=False)
  else:
    embed.add_field(name="ERROR", value=f"```ERROR: INVALID ID```", inline=False)

  await message.reply(embed=embed, mention_author=False)


async def end(message, endhangman):
  id = int(endhangman.group(1))
  author = hangmangames[id][1]
  embed = discord.Embed(
    title="Hangman",
    color=discord.Color.from_rgb(252, 164, 28)
  )
  embed.set_author(name=f"Gamebot")
  embed.set_footer(text=f"For all gamebot commands, type gamebot!help")
  if author == str(message.author):
    embed.add_field(name="Game over.", value=f"Hangman game number {id} was ended. The pattern was `{hangmangames[id][0]}`")
    hangmangames.pop(id)
  else:
    embed.add_field(name="", value=f"You do not have permission to delete this game")
  await message.reply(embed=embed, mention_author=False)