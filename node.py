from rules import Referee

class Node:

    # Class initialization
    def __init__(self, parent, board, turn):
        self.Q = 0  # sum of rollout outcomes
        self.N = 0  # number of visits
        self.parent = parent
        self.board = board
        self.sizeBoard = 19
        # root is always opponent's turn
        # Xem xét thăm dò node nào
        if turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        # no children has been expanded yet
        self.children = []
        self.expanded = False
        self.terminal = self.check_terminal()

    # Check if node is a leaf
    def check_terminal(self):
        rule = Referee(self.board)
        if rule.determine() is not None:
            return True
        return False
        # # check rows
        # for y in range(6):
        #     row = list(self.board[y, :])
        #     for x in range(4):
        #         if row[x:x+4].count(row[x]) == 4:
        #             if row[x] != 0:
        #                 return True
        # # check columns
        # for x in range(7):
        #     col = list(self.board[:, x])
        #     for y in range(3):
        #         if col[y:y+4].count(col[y]) == 4:
        #             if col[y] != 0:
        #                 return True
        # # check right diagonals
        # points = [(3, 0), (4, 0), (3, 1), (5, 0), (4, 1), (3, 2),
        #           (5, 1), (4, 2), (3, 3), (5, 2), (4, 3), (5, 3)]
        # for point in points:
        #     diag = list()
        #     for k in range(4):
        #         diag.append(self.board[point[0]-k, point[1]+k])
        #     if diag.count(1) == 4 or diag.count(2) == 4:
        #         return True
        # # check left diagonals
        # points = [(5, 3), (5, 4), (4, 3), (5, 5), (4, 4), (3, 3),
        #           (5, 6), (4, 5), (3, 4), (4, 6), (3, 5), (3, 6)]
        # for point in points:
        #     diag = list()
        #     for k in range(4):
        #         diag.append(self.board[point[0]-k, point[1]-k])
        #     if diag.count(1) == 4 or diag.count(2) == 4:
        #         return True
        # # no winner
        # return False
        # # no moves left
        # if list(self.board.flatten()).count(0) == 0:
        #     return True

    # Add child to node
    def add_child(self):
        # node already expanded
        if self.expanded:
            return
        # get board of every child
        child_board = list()
        for child in self.children:
            child_board.append(child.board)
        # find new child
        for i in range(self.sizeBoard):
            if self.board[self.sizeBoard - 1, i] == 0:
                for j in range(self.sizeBoard):
                    if self.board[j, i] == 0:
                        tmp = self.board.copy()
                        if self.turn == 1:
                            tmp[j, i] = 2
                            if child_board:
                                if not self.compare_children(tmp, child_board):
                                    self.children.append(Node(self, tmp, 1))
                                    return
                                else:
                                    break
                            else:
                                self.children.append(Node(self, tmp, 1))
                                return
                        else:
                            tmp[j, i] = 1
                            if child_board:
                                if not self.compare_children(tmp, child_board):
                                    self.children.append(Node(self, tmp, 2))
                                    return
                                else:
                                    break
                            else:
                                self.children.append(Node(self, tmp, 2))
                                return
        # no more children
        self.expanded = True
        return

    # True if children states are equal
    def compare_children(self, new_child, children):
        for child in children:
            if (new_child == child).all():
                return True
        return False

