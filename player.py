from common import Point

class Player:
  def __init__(self, player):
    self.player = player

  def move(self, row, column):
    return Point(row, column)

