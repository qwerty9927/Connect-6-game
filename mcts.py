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
        self.uct = 0

    # Main function for MCTS move computation
    def compute_move(self, root):
        time0 = time.time()
        playout = 0
        while(time.time() - time0) < self.t:
        # while playout != 500:
            # print(f"My node: {root.N} {root.Q}")
            # selection and expansion
            leaf = self.select(root) # có vấn đề
            # print("Selected: ", leaf)
            # simulation
            simulation_result = self.rollout(leaf)
            # backpropagation
            self.backpropagate(leaf, simulation_result)
            playout += 1
        # from next best state get move coordinates
        print("Playout: ", playout)
        selecteds = self.best_child(root)
        # print(f"Best node: {selected.N} {selected.Q}")
        # print(f"Best node board: {selected.board}")
        result = []
        for selected in selecteds:
            for j in range(self.sizeBoard):
                for i in range(self.sizeBoard):
                    # print(f"Selection {selected.board[j][i]}, Root {root.board[j][i]}, isMatch {selected.board[j][i] != root.board[j][i]}")
                    if selected.board[j][i] != root.board[j][i]:
                        result.append([j, i])
        return result

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
            # print("my node: ", node)
        # if node is terminal, return it
        if node.terminal:
            return node
        else:
            # expand node and return it for rollout
            node.add_child()
            # print("Inside select: ", node.children)

            return self.pick_unvisited(node.children) or node
        
            # if node.children:
            #     return self.pick_unvisited(node.children)
            # else:
            #     return node

    # Check if node is a leaf
    def fully_expanded(self, node):
        visited = True
        # max number of children a node can have
        if self.count_legal_actions(node) == len(node.children):
            # check if every node has been visited
            for child in node.children:
                if child.N == 0:
                    visited = False
            return visited
        else:
            return False
        # return False

    def count_legal_actions(self, node):
        # can_move = 0
        # for i in range(self.sizeBoard):
        #     for j in range(self.sizeBoard):
        #         if node.board[i, j] == 0:
        #             can_move += 1
        # return can_move
        # return (self.sizeBoard * self.sizeBoard) - np.count_nonzero(node.board)
        return np.sum(node.board == 0)
    
    # Return node with best uct value
    def select_uct(self, node):
        best_uct = -10000000
        best_node = None
        for child in node.children:
            uct = (child.Q/child.N) + 1.4*math.sqrt((math.log(node.N))/child.N)
            if uct > best_uct:
                best_uct = uct
                # print(uct)
                best_node = child
        # Avoid error if node has no children
        if best_node is None:
            return node
        else:
            return best_node

    # Policy for choosing unexplored nodes
    def pick_unvisited(self, children):
        for child in children:
            if child.N == 0:
                return child

    # Given a node, returns result of simulation
    def rollout(self, node):
        board = node.board
        # print(f"rollout board: {board}")
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
                    terminal = self.result(board, turn)
                    if terminal != 0:
                        # print("Terminal", terminal)
                        # print("Turn", node.turn)
                        # print("rollout", board)
                        return terminal
                # with no moves left return result
                else:
                    return self.result(board, turn)
        else:
            # if node is already terminal return result
            return self.result(board, turn)

    # Return all possible next states
    def get_moves(self, board, turn):
        moves = list()
        for i in range(self.sizeBoard):
            for j in range(self.sizeBoard):
                if board[i, j] == 0:
                    tmp = board.copy()
                    if turn == 1:
                        tmp[i, j] = 2
                    else:
                        tmp[i, j] = 1
                    moves.append(tmp)
        return moves
    
    def winner(self, board, turn):
        ##################################
        # vertical sequence detection
        ##################################
        chain_element = 6
        
        # loop over board columns
        for col in range(self.sizeBoard):
            # define winning sequence list
            winning_sequence = []
            
            # loop over board rows
            for row in range(self.sizeBoard):
                # if found same next element in the row
                if board[row, col] == turn:
                    # update winning sequence
                    winning_sequence.append((row, col))
                else:
                    winning_sequence = []
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == chain_element:
                    # return the game is won state
                    return board[row, col]
        
        ##################################
        # horizontal sequence detection
        ##################################
        
        # loop over board columns
        for row in range(self.sizeBoard):
            # define winning sequence list
            winning_sequence = []
            
            # loop over board rows
            for col in range(self.sizeBoard):
                # if found same next element in the row
                if board[row, col] == turn:
                    # update winning sequence
                    winning_sequence.append((row, col))
                else:
                    winning_sequence = []
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == chain_element:
                    # return the game is won state
                    return board[row, col]
    
        ##################################
        # 1st diagonal sequence detection
        ##################################
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(self.sizeBoard):
            # init column
            col = row
        
            # if found same next element in the row
            if board[row, col] == turn:
                # update winning sequence
                winning_sequence.append((row, col))
            else:
                winning_sequence = []
                
            # if we have 3 elements in the row
            if len(winning_sequence) == chain_element:
                # return the game is won state
                return board[row, col]
        
        ##################################
        # 2nd diagonal sequence detection
        ##################################
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(self.sizeBoard):
            # init column
            col = self.sizeBoard - row - 1
        
            # if found same next element in the row
            if board[row, col] == turn:
                # update winning sequence
                winning_sequence.append((row, col))
            else:
                winning_sequence = []
                
            # if we have 3 elements in the row
            if len(winning_sequence) == chain_element:
                # return the game is won state
                return board[row, col]
        
        # by default return non winning state
        return None
    
    # Get result score from board
    def result(self, board, turn):
        # winner = None
        # rule = Referee(board)
        # winner = rule.determine()

        winner = self.winner(board, turn)
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
        # print(f"Current node: {node.N} {node.Q}")
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
        second_best_node = None
        second_max_visit = 0
        # print(f"List node: {node.children}")
        for child in node.children:
            if child.N > max_visit:
                # print(f"Best child: {child.N} {child.Q}")
                max_visit = child.N
                best_node = child
            elif child.N > second_max_visit and child.N != max_visit:
                second_max_visit = child.N
                second_best_node = child
        print(f"N: {max_visit}")
        if best_node is not None:
            print(f"Best_node: {best_node.board} {best_node.N} {best_node.Q}")
        if second_best_node is not None:
            print(f"Second_best_node: {second_best_node.board} {second_best_node.N} {second_best_node.Q}")
        return [second_best_node, best_node]
