import numpy as np
from mcts import MCTS
from node import Node
from common import Point

# class MainBot():
#   def __init__(self):
#     self.player = 1

#   def move(self, row, column):
#     return Point(row, column)

#   def createGameBoard(self):
#     size = 7
#     # board = [[0 for i in range(6)] for j in range(7)]
#     board = np.zeros(shape=(19, 19))
#     return board
        
#   def main(self, board):
#     monteCarlo = MCTS(symbol=1, t=5)
#     board = self.createGameBoard()
#     inp = "next"
#     while(inp != "exit"):
#       if inp == "next":
#         root = Node(parent=None, board=board, turn=monteCarlo.symbol)
#         move = monteCarlo.compute_move(root)
#         print(f"Row {move[0]}, Column {move[1]}")
#         board[move[0], move[1]] = 1
#         print(f"Board {board}")
#     # return move
#       inp = input()

# if __name__ == '__main__':
#   bot = MainBot()
#   bot.main(bot.createGameBoard())

# test
class MainBot():
  def __init__(self, player, board):
    self.player = player
    self.board = board
    self.monteCarlo = MCTS(symbol=1, t=5)

  def move(self, row, column):
    return Point(row, column)

  def createGameBoard(self):
    # board = [[0 for i in range(6)] for j in range(7)]
    board = np.zeros(shape=(19, 19))
    return board
        
  def main(self):
    root = Node(parent=None, board=self.board, turn=self.monteCarlo.symbol)
    move = self.monteCarlo.compute_move(root)
    return move
