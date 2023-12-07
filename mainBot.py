import numpy as np
from mcts import MonteCarloTreeSearchNode, Connect6
from common import Point

class MainBot():
  def __init__(self, player):
    self.player = player

  def move(self, row, column):
    return Point(row, column)

  def main(self, board, opposite):
    game = Connect6(board, opposite, 0)
    mcts = MonteCarloTreeSearchNode(game)
    action = mcts.best_action()
    return tuple(int(element) for element in action)

