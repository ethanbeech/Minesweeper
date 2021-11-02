import random

### Classes for program
class BoardTile(object): # Object for individual tiles on the board
	def __init__(self):
		self.is_mine = False
		self.is_flagged = False
		self.is_question = False
		self.is_revealed = False
		self.adjacent_mines = 0

	def __str__(self):
		if self.is_revealed == False:
			if self.is_flagged:
				return " ! "
			elif self.is_question:
				return " ? "
			else:
				return "   "
		else:
			if self.is_mine:
				return " M "
			else:
				return " " + str(self.adjacent_mines) + " "

	# Define series of functions to return variables (allows for later modification)
	def createMine(self):
		self.is_mine = True

	def checkIsMine(self):
		return self.is_mine

	def incrementAdjacentCount(self):
		self.adjacent_mines += 1

	# Allow a tile to show it's number/'M' on the board
	def revealTile(self):
		self.is_revealed = True

	def questionTile(self):
		if self.is_revealed:
			print("Cannot place a question mark on a revealed tile")
		else:
			self.is_flagged = False
			self.is_question = not self.is_question

	def flagTile(self):
		if self.is_revealed:
			print("Cannot place a flag on a revealed tile")
		else:
			self.is_flagged = not self.is_flagged
			self.is_question = False

	

class Board:
	def __init__(self,board_size,start_no_mines):
		# Transfer parameters to object
		self.board_size = board_size
		self.start_no_mines = start_no_mines
		self.tiles_to_clear = self.board_size[0]*self.board_size[1] - self.start_no_mines	

		# Create board
		self.board = [[]*5]*5
		self.board = [[BoardTile() for i in range(board_size[0])] for j in range(board_size[1])]

		# Detemine tiles with mines
		no_active_mines = 0

		while no_active_mines < self.start_no_mines:
			# Choose coordinates
			x = random.randint(0,board_size[0]-1)
			y = random.randint(0,board_size[1]-1)
			# Check if tile is a mine and creates if not
			if not bool(self.board[x][y].checkIsMine()):
				self.board[x][y].createMine()
				no_active_mines += 1
				# Update surrounding mine counters
				surroundingCoords = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1)]
				for coord in surroundingCoords:
					if 0 <= coord[0] < self.board_size[0] and 0 <= coord[1] < self.board_size[1]:
						self.board[coord[0]][coord[1]].incrementAdjacentCount()

	def __str__(self):
		# Define starting string to append to with other lines
		board_image = ""
		# Continuous horizontal line to seperate tiles
		lineHorizontal = "----" * self.board_size[1] + "\n"
		# Iterate down board
		for y in range(self.board_size[1]-1,-1,-1):
			board_image += lineHorizontal
			currentLine = ""
			# Iterate along rows
			for x in range(self.board_size[0]):
				currentLine += "|" + str(self.board[x][y])
			currentLine += "|\n"
			board_image += currentLine
		board_image += lineHorizontal
		return board_image

	# For when player chooses to flip a tile (not for flag/question)
	def trigger_tile(self,x,y):
		# Creates a queue for all tiles that need to be checked
		check_queue = {(x,y)}
		# Repeats until check_queue is emptied
		while len(check_queue) != 0:
			# Takes new set of coords from check_queue and remove from the set
			coords = next(iter(check_queue))
			check_queue.remove(coords)
			x = coords[0]
			y = coords[1]
			self.board[x][y].is_revealed = True
			is_mine = bool(self.board[x][y].checkIsMine())
			if is_mine:
				print("MINE DETONATED")
				print("GAME OVER")
				return False # Returns for "continue_game"
			else:
				# Clear specified tiles
				print("Tile cleared at ({},{})".format(x,y))
				self.tiles_to_clear -= 1
				# Clear surrounding tiles if adjacent_bombs == 0
				if int(self.board[x][y].adjacent_mines) == 0:
					surroundingCoords = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1)]
					for surroundingCoord in surroundingCoords:
						if 0 <= surroundingCoord[0] < self.board_size[0] and 0 <= surroundingCoord[1] < self.board_size[1]:
							if bool(self.board[surroundingCoord[0]][surroundingCoord[1]].is_revealed) == False:
								check_queue.add((surroundingCoord[0],surroundingCoord[1]))

		return True # Returns for "continue_game"

	def question_tile(self,x,y):
		self.board[x][y].questionTile()

	def flag_tile(self,x,y):
		self.board[x][y].flagTile()

	def game_conclude(self):
		for x in range(self.board_size[0]):
			for y in range(self.board_size[1]):
				self.board[x][y].is_revealed = True

def initialiseGame():
	# Print instructions
	print("")
	difficultyChoice = str(input("Please hit enter to continue with default settings, or type 'custom' to choose custom values: "))
	if difficultyChoice == "custom":
		userInputsValid = False
		while not userInputsValid:
			width = int(input("Enter board width: "))
			height = int(input("Enter board height: "))
			no_mines = int(input("Enter number of mines: "))
			# Set series of validation tests in order to accept/reenter settings
			valid1 = (no_mines < width * height - 1)
			valid2 = (width > 0)
			valid3 = (height > 0)
			if valid1 and valid2 and valid3:
				userInputsValid = True
		# Define instance of Board
		board = Board([width,height],no_mines)
	else:
		# Define instance of Board with default settings (default values found online)
		board = Board([16,16],40)
	return board


board = initialiseGame()
print(int(board.board[1][1].adjacent_mines))

game_continue = True

while board.tiles_to_clear > 0 and game_continue:
	print(board)
	userInputsValid = False
	while not userInputsValid:
		xInput = int(input("Please input an x value")) - 1
		yInput = int(input("Please input a y value")) - 1
		if 0 <= xInput <= board.board_size[0] and 0 <= yInput <= board.board_size[1]:
			userInputsValid = True
		else:
			print("Invalid coordinates")
	# Print instructions and take response
	triggerType = str(input("Type F to flag, Q to place a question mark, or anything else to clear (not case specific)")).lower()
	if triggerType == "f":
		board.flag_tile(xInput,yInput)
	elif triggerType == "q":
		board.question_tile(xInput,yInput)
	else:
		game_continue = board.trigger_tile(xInput,yInput)

# Print board with last action and after reavealling all tiles
print(board)
board.game_conclude()
print(board)