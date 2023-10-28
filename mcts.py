import numpy as np
import random
import time
import math
from rules import Referee

class MCTS:

    # Class initialization
    def __init__(self, symbol, t, sizeBoard = 19):
        self.symbol = symbol
        self.t = t
        self.sizeBoard = sizeBoard

    # Main function for MCTS move computation
    def compute_move(self, root):
        time0 = time.time()
        playout = 0
        while(time.time() - time0) < self.t:
            # selection and expansion
            leaf = self.select(root) # có vấn đề
            # simulation
            simulation_result = self.rollout(leaf)
            # backpropagation
            self.backpropagate(leaf, simulation_result)
            playout += 1
        # from next best state get move coordinates
        print("Playout: ", playout)
        selected = self.best_child(root)
        # print(f"Best node: {selected.board}")
        for j in range(self.sizeBoard):
            for i in range(self.sizeBoard):
                # print(f"Selection {selected.board[j][i]}, Root {root.board[j][i]}, isMatch {selected.board[j][i] != root.board[j][i]}")
                if selected.board[j][i] != root.board[j][i]:
                    return (j, i)

    # Node traversal
    def select(self, node):
        # if all children of node has been expanded
        # select best one according to uct value
        while(self.fully_expanded(node)):
            tmp = self.select_uct(node)
            # if select_uct returns back the node break
            if tmp == node:
                break
            # if not, keep exploring the tree
            else:
                node = tmp
        # if node is terminal, return it
        if node.terminal:
            return node
        else:
            # expand node and return it for rollout
            node.add_child()
            if node.children:
                return self.pick_unvisited(node.children)
            else:
                return node

    # Return node with best uct value
    def select_uct(self, node):
        best_uct = -10000000
        best_node = None
        for child in node.children:
            uct = (child.Q/child.N) + 1.4*math.sqrt((math.log(node.N))/child.N)
            if uct > best_uct:
                best_uct = uct
                best_node = child
        # Avoid error if node has no children
        if best_node is None:
            return node
        else:
            return best_node

    # Check if node is a leaf
    def fully_expanded(self, node):
        visited = True
        # max number of children a node can have
        if list(node.board[self.sizeBoard - 1]).count(0) == len(node.children):
            # check if every node has been visited
            for child in node.children:
                if child.N == 0:
                    visited = False
            return visited
        else:
            return False

    # Policy for choosing unexplored nodes
    def pick_unvisited(self, children):
        for child in children:
            if child.N == 0:
                return child

    # Given a node, returns result of simulation
    def rollout(self, node):
        board = node.board
        turn = node.turn
        if not node.terminal:
            while(True):
                # switch turn
                if turn == 1:
                    turn = 2
                else:
                    turn = 1
                # get moves from current board
                moves = self.get_moves(board, turn)
                if moves:
                    # select next board randomly
                    board = random.choice(moves)
                    # check if state is terminal
                    terminal = self.result(board)
                    if terminal != 0:
                        # print("rollout", board)
                        return terminal
                # with no moves left return result
                else:
                    return self.result(board)
        else:
            # if node is already terminal return result
            return self.result(board)

    # Return all possible next states
    def get_moves(self, board, turn):
        moves = list()
        for i in range(self.sizeBoard):
            if board[self.sizeBoard - 1, i] == 0:
                for j in range(self.sizeBoard):
                    if board[j, i] == 0:
                        tmp = board.copy()
                        if turn == 1:
                            tmp[j, i] = 2
                        else:
                            tmp[j, i] = 1
                        moves.append(tmp)
                        break
        return moves

    # Get result score from board
    def result(self, board):
        # winner = None
        rule = Referee(board)
        winner = rule.determine()
        # # check rows
        # for y in range(6):
        #     row = list(board[y, :])
        #     for x in range(4):
        #         if row[x:x+4].count(row[x]) == 4:
        #             if row[x] != 0:
        #                 winner = row[x]
        # # check columns
        # for x in range(7):
        #     col = list(board[:, x])
        #     for y in range(3):
        #         if col[y:y+4].count(col[y]) == 4:
        #             if col[y] != 0:
        #                 winner = col[y]
        # # check right diagonals
        # points = [(3, 0), (4, 0), (3, 1), (5, 0), (4, 1), (3, 2),
        #           (5, 1), (4, 2), (3, 3), (5, 2), (4, 3), (5, 3)]
        # for point in points:
        #     diag = list()
        #     for k in range(4):
        #         diag.append(board[point[0]-k, point[1]+k])
        #     if diag.count(1) == 4 or diag.count(2) == 4:
        #         winner = diag[k]
        # # check left diagonals
        # points = [(5, 3), (5, 4), (4, 3), (5, 5), (4, 4), (3, 3),
        #           (5, 6), (4, 5), (3, 4), (4, 6), (3, 5), (3, 6)]
        # for point in points:
        #     diag = list()
        #     for k in range(4):
        #         diag.append(board[point[0]-k, point[1]-k])
        #     if diag.count(1) == 4 or diag.count(2) == 4:
        #         winner = diag[k]
        # Tie
        if winner is None:
            return 0
        else:
            # Win
            if self.symbol == winner:
                return 1
            # Defeat
            else:
                return -1

    # Resursive function to update number of visits
    # and score of each node from leaf to root
    def backpropagate(self, node, result):
        # add result when AI's turn
        if node.turn == self.symbol:
            node.Q += result
        # or else subtract it
        else:
            node.Q -= result
        # increment visit number by 1
        node.N += 1
        # stop if node is root
        if node.parent is None:
            return
        else:
            # call function recursively on parent
            self.backpropagate(node.parent, result)

    # Returns root child with largest number of visits
    def best_child(self, node):
        max_visit = 0
        best_node = None
        for child in node.children:
            if child.N > max_visit:
                max_visit = child.N
                best_node = child
        return best_node
