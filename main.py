import discord
import os
import random
import re

import battleship
import tictactoe
import hangman

client = discord.Client()

@client.event
async def on_ready():
  print('{0.user} has connected'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if "gamebot!help" in message.content:
    embed = discord.Embed(
      title="Gamebot",
      color=discord.Color.from_rgb(252, 164, 28)
    )
    embed.add_field(name="*The best way to play games on Discord*", value="We have relocated to https://actiniumn404.github.io/Gamebot/ because of the charactor limit, so please go there.")
    embed.set_author(name=f"Gamebot")
    await message.reply(embed=embed, mention_author=False)

  if "<@!886304776042737675>" in message.content:
    await message.channel.send("Hello! It's a good day for a game right?")

  rps = re.match("!rps (r|p|s)", message.content)
  if rps:
    move = str(rps.group(1)).lower()
    choice = random.choice(["rock", "paper", "scissors"])
    j = {
      "r":{
        "rock":"we tied",
        "paper":"I won",
        "scissors":"you won"
      },
      "p":{
        "rock":"you won",
        "paper":"we tied",
        "scissors":"I won"
      },
      "s":{
        "rock":"I won",
        "paper":"you won",
        "scissors":"we tied"
      }
    }

    convert = {"r":"rock", "s":"scissors", "p":"paper"}

    embed = discord.Embed(
      title="Rock, Paper, Scissors",
      color=discord.Color.from_rgb(252, 164, 28)
    )
    embed.set_author(name=f"Gamebot")
    if move in ["r", "p", "s"]:
      embed.add_field(name="Results", value=f"You picked {convert[move]} and I picked {choice}. Therefore, {j[move][choice]}.")
    else:
      embed.add_field(name="Results", value=f"ERROR. Your choice was not understood. Please type either r, p, or s for rock, paper, and scissors respectively")
    embed.set_footer(text=f"For all gamebot commands, type gamebot!help")

    await message.reply(embed=embed, mention_author=False)


  newhangman = re.match("!newhangman (.*)", message.content)
  if newhangman:
    await hangman.new(message, newhangman)

  hangmanguess = re.match("!hangman ([0-9]+) guess ([a-zA-Z]+)", message.content)
  if hangmanguess:
    await hangman.guess(message, hangmanguess)
  
  endhangman = re.match("!hangman ([0-9]+) end game", message.content)
  if endhangman:
    await hangman.end(message, endhangman)

  # Tic tack toe
  ttt = re.match("!newtictactoe (.*)", message.content)
  if ttt:
    await tictactoe.new(message, ttt)

  tttinvite = re.match("!tictactoe ([0-9]+) (accept|decline)", message.content)
  if tttinvite:
    await tictactoe.invite(message, tttinvite)

  tttplay = re.match("!tictactoe ([0-9]+) play ([A-Ca-c])([1-3])", message.content)
  if tttplay:
    await tictactoe.play(message, tttplay)

  # battleship
  newship = re.match("!newbattleship\n```\n(.*)\n```", message.content, flags=re.MULTILINE | re.DOTALL)
  if newship:
    matrix = newship.group(1)
    matrix = matrix.split("\n")
    matrix = [x.replace("_", " ").split(" ") for x in matrix]
    await battleship.new(message, matrix)    


client.run(os.getenv('TOKEN'))