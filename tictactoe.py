import discord
import random

tictactoe = {}
async def new(message, ttt):
	embed = discord.Embed(
		title="Tic tac toe",
		color=discord.Color.from_rgb(252, 164, 28)
	)
	embed.set_author(name=f"Gamebot")
	embed.set_footer(text=f"For all gamebot commands, type gamebot!help")

	if "<@!" not in ttt.group(1):
		embed.add_field(name="ERROR", value=f"`YOU DIDN'T @ MENTION YOUR CHALLENGER`", inline=False)
		await message.reply(embed=embed, mention_author=False)
		return

	while True:
		id = random.randint(10000, 99999)
		if id not in list(tictactoe.keys()):
			break
	tictactoe[id] = [int(message.author.id), int(ttt.group(1)[3:-1]), False, [" "]*9, 0]

	embed.add_field(name="An invitation", value=f"{ttt.group(1)}, you have been challenged to tic tac toe game number {str(id)} by {str(message.author)}. Will you decline or accept?", inline=False)
	embed.add_field(name="How to accept/decline", value=f"Please type `!tictactoe {str(id)} decline` to decline and `!tictactoe {str(id)} accept` to accept", inline=True)
	await message.reply(embed=embed, mention_author=False)


async def invite(message, tttinvite):
  embed = discord.Embed(
    title="Tic tac toe",
    color=discord.Color.from_rgb(252, 164, 28)
  )
  embed.set_author(name=f"Gamebot")
  embed.set_footer(text=f"For all gamebot commands, type gamebot!help")
  id = int(tttinvite.group(1))
  acdl = tttinvite.group(2)
  if id not in list(tictactoe.keys()):
    embed.add_field(name="ERROR", value=f"`ERROR: ID {str(id)} DOES NOT EXIST`")
  elif str(message.author.id) != str(tictactoe[id][1]):
    embed.add_field(name="ERROR", value=f"ERROR: <@!{str(message.author.id)}> IS NOT EQUAL TO <@!{tictactoe[id][1]}>")
  else:
    if acdl == "decline":
      tictactoe.pop(id)
    else:
      board = f"""
    1   2   3
  +-----------+
A | {tictactoe[id][3][0]} | {tictactoe[id][3][1]} | {tictactoe[id][3][2]} |
  |-----------|
B | {tictactoe[id][3][3]} | {tictactoe[id][3][4]} | {tictactoe[id][3][5]} |
  |-----------|
C | {tictactoe[id][3][6]} | {tictactoe[id][3][7]} | {tictactoe[id][3][8]} |
  +-----------+
"""
      tictactoe[id][2] = True
      embed.add_field(name="Game Accepted", value=f"The game has been accepted by {str(message.author)}. We will alternate between <@!{tictactoe[id][0]}> (as `X`) and <@!{tictactoe[id][1]}> (as `O`). It is now <@!{tictactoe[id][tictactoe[id][4]]}>'s turn. What will you play?", inline=False)
      embed.add_field(name="The current board", value=f"```{board}```", inline=False)
      embed.add_field(name="How to play a move", value=f"Look at the board above. You will see a coordinate system. To play a move, simply type `!tictactoe {id} play COORDINATE` with the coordinate being something like C3", inline=False)
  
  await message.reply(embed=embed, mention_author=False)


async def play(message, tttplay):
  embed = discord.Embed(
    title="Tic tac toe",
    color=discord.Color.from_rgb(252, 164, 28)
  )
  embed.set_author(name=f"Gamebot")
  embed.set_footer(text=f"For all gamebot commands, type gamebot!help")
  id = int(tttplay.group(1))
  convert = {"A":-1, "B":2, "C":5}
  row = convert[str(tttplay.group(2)).upper()]
  col = int(tttplay.group(3))
  if id not in list(tictactoe.keys()):
    embed.add_field(name="ERROR", value="`ERROR: ID DOES NOT EXIST`")
  elif int(message.author.id) not in [tictactoe[id][0], tictactoe[id][1]]:
    embed.add_field(name="ERROR", value="`ERROR: PLAYER NOT IN CAN PLAY LIST`")
  elif (tictactoe[id][4] == 0 and int(message.author.id) != tictactoe[id][0]) or (tictactoe[id][4] == 1 and int(message.author.id) != tictactoe[id][1]):
    embed.add_field(name="ERROR", value="`ERROR: IT IS NOT YOUR TURN YET.`")
  else:
    if tictactoe[id][3][row+col] != " ":
    	embed.add_field(name="ERROR", value="`ERROR: DON'T BE THAT JERK WHO REPLACES A PREVIOUS MOVE`")
    else:
      tictactoe[id][3][row+col] = ("X" if tictactoe[id][4] == 0 else "O")
      tictactoe[id][4] = 1 - tictactoe[id][4]
      temp = ("X" if tictactoe[id][4] == 0 else "O")
      board = f"""
    1   2   3
  +-----------+
A | {tictactoe[id][3][0]} | {tictactoe[id][3][1]} | {tictactoe[id][3][2]} |
  |-----------|
B | {tictactoe[id][3][3]} | {tictactoe[id][3][4]} | {tictactoe[id][3][5]} |
  |-----------|
C | {tictactoe[id][3][6]} | {tictactoe[id][3][7]} | {tictactoe[id][3][8]} |
  +-----------+
""" 
      # Check if it is a win
      x = tictactoe[id][3]
      winch = [
        x[0:3], 
        x[3:6], 
        x[6:9], 
        [x[0], x[3], x[6]], 
        [x[1], x[4], x[7]], 
        [x[2], x[5], x[8]], 
        [x[2], x[4], x[6]], 
        [x[0], x[4], x[8]]
      ]
      embed.add_field(name="The current board", value=f"```{board}```", inline=False)
      if any([x.count("X") == 3 for x in winch]) or any([x.count("O") == 3 for x in winch]):
        embed.add_field(name="We have a winner", value=f"Congragulations {str(message.author)}, you have won tic tac toe game number {id} :slight_smile:")
        tictactoe.pop(id)
      elif " " not in x:
        embed.add_field(name="The Game Has Ended", value=f"As fun as this game was, it cannot last forever. This game has ended with a tie, where neither `X` or `O` won. Have a great day!")
        tictactoe.pop(id)
      # End check
      else:
        embed.add_field(name="Move played", value=f"{str(message.author)}(`{temp}`) has just played the move {str(tttplay.group(2)).upper()+str(row)}. It is now <@!{tictactoe[id][tictactoe[id][4]]}>'s turn. What will you play?", inline=False)
        embed.add_field(name="How to play a move", value=f"Look at the board above. You will see a coordinate system. To play a move, simply type `!tictactoe {id} play COORDINATE` with the coordinate being something like C3", inline=False)
  await message.reply(embed=embed, mention_author=False)