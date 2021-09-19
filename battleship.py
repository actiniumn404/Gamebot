def b_validate(message, matrix):
  err = False
  checklist = [1, 2, 3, 4, 5]
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
                          error[1].append(True)
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
                          return "Invalid! There is a *hole* in your ship"
                      else:
                          return "Invalid number of pegs for a ship"


                  for shipConponent in cols:
                      if matrix[shipConponent][row] == str(j):
                          matrix[shipConponent][row] = " "
                  checklist.pop(checklist.index(j))
              else:
                  return "You have either placed a ship that you have already placed, or have placed a ship with an invalid number of spots. Only ships that occupy 1-5 spots are allowed."

  if checklist != []:
      return "You have not placed down all your ships yet."
  elif not err:
      return "true"