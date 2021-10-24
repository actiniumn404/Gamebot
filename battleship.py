import discord
import random

games = {}

def validate(matrix):
  err = False
  checklist = [1, 2, 3, 4, 5]
  letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
  for col in range(len(matrix)):
      for row in range(len(matrix[col])):
          j = matrix[col][row]
          if str(j).isdigit():
              if int(j) in checklist:
                  # Rows
                  j = int(j)
                  cols = []
                  for x in range(col - j, col + j):
                      if x >= 0 and x < len(matrix[col]):
                          cols.append(matrix[x][row])

                  locs = [
                      matrix[col][(row - j + 1 if row - j + 1 >= 0 else 0):(row + j if row + j < len(matrix[col]) else len(matrix[col]) - 1)],
                      cols
                  ]
                  error = [[], []]
                  whichloc = None
                  cols = list(range(1, 6))
                  cols.remove(int(j))
                  for i, ship in enumerate(locs):
                      if " " in "".join([str(x) for x in ship]).strip(" "+"".join([str(x) for x in cols])):
                          error[0].append(True)
                      elif "".join([str(x) for x in ship]).count(str(j)) != j:
                          error[1].append("".join([str(x) for x in ship]).count(str(j)))
                      else:
                          whichloc = 0
                  cols = []
                  for x in range(row - j + 1, row + j):
                      if x >= 0 and x < len(matrix[col]):
                          cols.append(x)

                  if whichloc == 0:
                      for shipConponent in range((row - j + 1 if row - j + 1 >=0 else 0), (row + j if row + j < len(matrix[col]) else len(matrix[col]) - 1)):
                          if matrix[col][shipConponent] == str(j):
                              matrix[col][shipConponent] = " "
                  elif whichloc == 1:
                      for shipConponent in range(row - j + 1, row + j):
                          if matrix[shipConponent][row] == str(j) and (shipConponent >= 0 and shipConponent < len(matrix[col])):
                              matrix[shipConponent][row] = " "
                  else:
                      err = True
                      if any(error[0]):
                          return f"There is a hole in ship #{str(j)} ({letters[col]}{str(row+1)})"
                          #return 1
                      else:
                          return f"Why does the ship that takes up {str(j)} spaces ({letters[col]}{str(row+1)}) take up not that many spaces???"
                          #return 2


                  for shipConponent in cols:
                      if matrix[shipConponent][row] == str(j):
                          matrix[shipConponent][row] = " "
                  checklist.pop(checklist.index(j))
              else:
                  return f"You have placed more than one {str(j)} ship at ({letters[col]}{str(row+1)}"
                  #return 3

  if checklist != []:
      x = ", ".join( list( map(str, checklist) ) )
      return f"You have not placed down ships { x } yet"
      #return 4
  elif not err:
      return 0


async def new(message, challenger):
	embed = discord.Embed(
		title="Tic tac toe",
		color=discord.Color.from_rgb(252, 164, 28)
	)
	embed.set_author(name=f"Gamebot")
	embed.set_footer(text=f"For all gamebot commands, type gamebot!help")
	if "<@!" not in challenger:
		embed.add_field(name="An invitation", value=f"", inline=False)
		return

		

	await message.reply(embed=embed, mention_author=False)