import tkinter as tk
import numpy as np
from rules import Referee
from logger import MoveLogger
from common import Move
from config import AIBot
from mainBot import MainBot
from player import Player

STONE_NAME = ['', 'White (O)', 'Black (X)']

class Game:
  def __init__(self, size = 19) -> None:
    self.bot_set = [None]
    # self.board = [[0 for x in range(size)] for y in range(size)]
    self.board = np.zeros(shape=(19, 19))
    self.referee = Referee(self.board)
    self.nth_move = 1
    self.player = 2  # 1=white 2=black. black moves first
    self.current_player_moved_count = 2  # at first time, black can only move once.
    self.logger = MoveLogger()
    self.selectAble = True
    self.stores = []
    self.currentIndex = -1

    # Main screen
    self.myScreen = tk.Tk()
    self.myScreen.title('Connect 6 game')
    self.myScreen.maxsize(900, 600)
    self.myScreen.config(background="skyblue")
    self.arrayPos = self.left(size)    
    self.right()   
    
    # Toplevel
    self.startTopLevelScreen()

    self.myScreen.mainloop()
    
  def start1vs1(self):
    self.bot_set = [None, Player(1), Player(2)]

  def startWithBot(self):
    self.bot_set = [None, MainBot(1, self.board), Player(2)]

  def startGame(self, callback):
    self.myScreen.deiconify()
    self.startScreen.destroy()
    callback()

  # Start top level screen
  def startTopLevelScreen(self):
    self.startScreen = tk.Toplevel(self.myScreen)
    self.startScreen.title("Start Connect 6 game")
    self.startScreen.geometry("200x200")
    tk.Button(self.startScreen, text="Start 1 vs 1", width=120, command=lambda: self.startGame(self.start1vs1)).pack()
    tk.Button(self.startScreen, text="Start vs bot", width=120, command=lambda: self.startGame(self.startWithBot)).pack()
    tk.Button(self.startScreen, text="Load record", width=120).pack()
    tk.Button(self.startScreen, text="Close", width=120, command=self.myScreen.destroy).pack()

    self.myScreen.withdraw()
    self.startScreen.protocol("WM_DELETE_WINDOW", self.myScreen.destroy)

  # Left
  def left(self, size):
    arrayPos = []
    self.leftFrame = tk.Frame(self.myScreen, width=650, height= 600)
    self.leftFrame.grid(row=0, column=0, padx=10, pady=5)
    for i in range(size):
      subArray = []
      for j in range(size):
        button = tk.Button(self.leftFrame, text=" ", width=2, height=1, bg="#EFB265", command=lambda i = i, j = j: self.selectPos(i, j))
        button.grid(row=i, column=j)
        subArray.append(button)
      arrayPos.append(subArray)
    return arrayPos

  # Right
  def right(self):
    self.rightFrame = tk.Frame(self.myScreen, width= 200, height=600, background="green")
    self.rightFrame.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(self.rightFrame, text="Message", font=50).grid(row=0, column=0, padx=5)

    self.message = tk.Message(self.rightFrame, width=150, text="Hello world")
    self.message.grid(row=1, column=0, padx=5, pady=10)

    tk.Label(self.rightFrame, text="Tool bar", font=50).grid(row=2, column=0, padx=5, pady=5)
    self.toolBar = tk.Frame(self.rightFrame, width=180, height= 200)
    self.toolBar.grid(row=3, column=0, padx=5, pady=5)
    tk.Button(self.toolBar, text="Undo", width=20, command=self.undo).pack()
    tk.Button(self.toolBar, text="Redo", width=20, command=self.redo).pack()
    tk.Button(self.toolBar, text="New game", width=20).pack()

    tk.Button(self.toolBar, text="Close", command=self.myScreen.destroy)

# Handle game
  def exit_game(self, logger: MoveLogger, won_bot=None):
    if won_bot is not None:
      self.message["text"] = f"Winner is {STONE_NAME[won_bot.player]}"
      logger.log_winner(won_bot.player)
      print('{} won!!'.format(STONE_NAME[won_bot.player]))
    else:
      print('No one won.')

    # logger.save_to_file()

  def selectPos(self, row, column):
    # Chon roi khong chon nua
    if(self.referee.can_place(row, column) and self.selectAble):
      self.arrayPos[row][column]["bg"] = "#000" if self.player == 2 else "#fff"

      # x: column, y: row
      x, y = self.bot_set[self.player].move(column, row)
      print(f"Player {self.player}")
      print(f"Column {x}, Row {y}")
       
      # place stone // Ghi log
      self.board[y][x] = self.player
      self.logger.log(x, y, self.player)
      self.referee.update(x, y, self.player)
      
       # Store status
      self.stores = self.stores[0:self.currentIndex + 1]
      self.stores.append(Move(y, x, self.player, self.current_player_moved_count).__dict__)
      self.currentIndex += 1

      # Determine won
      if self.isWin():
        return
     
      # Reset status
      if self.current_player_moved_count == 2:
          # Change turn : a player can move 2 times per turn.
          self.nth_move += 1
          self.current_player_moved_count = 0
          self.player = 2 if self.player == 1 else 1
      self.current_player_moved_count += 1


      self.stateGame(self.player)

      
      if(isinstance(self.bot_set[self.player], MainBot)):
        row, column = self.bot_set[self.player].main()
        self.selectPos(row, column)

      # print("Game", self.stores)

    elif not self.referee.can_place(row, column) and self.selectAble:
      self.message["text"] = "Try again in another place."

  def undo(self):
    if(self.currentIndex > 0):
      last_y = self.stores[self.currentIndex]["row"]
      last_x = self.stores[self.currentIndex]["column"]
      current_y = self.stores[self.currentIndex - 1]["row"]
      current_x = self.stores[self.currentIndex - 1]["column"]
      player = self.stores[self.currentIndex]["player"]
      current_player_moved_count = self.stores[self.currentIndex]["current_player_moved_count"]
      self.board[last_y][last_x] = 0
      self.referee.undo(last_x, last_y, current_x, current_y, 0)
      self.current_player_moved_count = current_player_moved_count
      self.player = player
      self.stateGame(player)
      self.undoState(last_y, last_x)
      self.currentIndex -= 1

    elif(self.currentIndex == 0):
      last_y = self.stores[self.currentIndex]["row"]
      last_x = self.stores[self.currentIndex]["column"]
      player = self.stores[self.currentIndex]["player"]
      current_player_moved_count = self.stores[self.currentIndex]["current_player_moved_count"]
      self.board[last_y][last_x] = 0
      self.referee.undo(last_x, last_y, 0, 0, 0)
      self.current_player_moved_count = current_player_moved_count
      self.player = player
      self.stateGame(player)
      self.undoState(last_y, last_x)
      self.currentIndex = -1

  def undoState(self, row, column):
    self.arrayPos[row][column]["bg"] = "#EFB265"
    if(self.won_player):
      self.selectAble = True
      self.won_player = None

  def redo(self):
    # print(f"Current {self.currentIndex} --- len {len(self.stores) - 1}")
    if(self.currentIndex < len(self.stores) - 1):
      self.currentIndex += 1
      current_y = self.stores[self.currentIndex]["row"]
      current_x = self.stores[self.currentIndex]["column"]
      player = self.stores[self.currentIndex]["player"]
      current_player_moved_count = self.stores[self.currentIndex]["current_player_moved_count"]
      self.referee.redo(current_x, current_y, player)

      self.board[current_y][current_x] = player
      self.current_player_moved_count = current_player_moved_count
      self.player = player
      self.stateGame(player)
      self.redoState(current_y, current_x)
      self.isWin()

  def redoState(self, row, column):
    self.arrayPos[row][column]["bg"] = "#000" if self.player == 2 else "#fff"

  def stateGame(self, player):
    self.message["text"] = f"{STONE_NAME[player]} do next step."

  def isWin(self):
    self.won_player = self.referee.determine()
    if self.won_player is not None:
        self.won_player = int(self.won_player)
        self.exit_game(self.logger, self.bot_set[self.won_player])
        self.selectAble = False
        return True
    return False

