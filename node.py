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
        if turn == 1:
            self.turn = 2
        else:
            self.turn = 1
            
        # no children has been expanded yet
        self.children = []
        self.expanded = False
        self.terminal = self.check_terminal()

    def winner(self, board):
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
                if board[row, col] == self.turn:
                    # update winning sequence
                    winning_sequence.append((row, col))
                else:
                    winning_sequence = []
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == chain_element:
                    # return the game is won state
                    return True
        
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
                if board[row, col] == self.turn:
                    # update winning sequence
                    winning_sequence.append((row, col))
                else:
                    winning_sequence = []
                    
                # if we have 3 elements in the row
                if len(winning_sequence) == chain_element:
                    # return the game is won state
                    return True
    
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
            if board[row, col] == self.turn:
                # update winning sequence
                winning_sequence.append((row, col))
            else:
                winning_sequence = []
                
            # if we have 3 elements in the row
            if len(winning_sequence) == chain_element:
                # return the game is won state
                return True
        
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
            if board[row, col] == self.turn:
                # update winning sequence
                winning_sequence.append((row, col))
            else:
                winning_sequence = []
                
            # if we have 3 elements in the row
            if len(winning_sequence) == chain_element:
                # return the game is won state
                return True
        
        # by default return non winning state
        return False
    
    # Check if node is a leaf
    def check_terminal(self):
        if self.winner(self.board):
            return True

        # rule = Referee(self.board)
        # if rule.determine() is not None:
        #     return True
        
        if list(self.board.flatten()).count(0) == 0:
            return True
        return False

    # Add child to node
    def add_child(self):
        # node already expanded
        if self.expanded:
            return
        
        for i in range(self.sizeBoard):
            for j in range(self.sizeBoard):
                if self.board[i, j] == 0:
                    tmp = self.board.copy()
                    if self.turn == 1:
                        tmp[i, j] = 2
                        self.children.append(Node(self, tmp, 1))
                        # print("Node: 1")
                    else:
                        tmp[i, j] = 1
                        self.children.append(Node(self, tmp, 2))
                        # print("Node: 2")
        # get board of every child
        # child_board = list()
        # for child in self.children:
        #     child_board.append(child.board)
        # # find new child
        # for i in range(self.sizeBoard):
        #         for j in range(self.sizeBoard):
        #             if self.board[i, j] == 0:
        #                 tmp = self.board.copy()
        #                 if self.turn == 1:
        #                     tmp[i, j] = 2
        #                     if child_board:
        #                         if not self.compare_children(tmp, child_board):
        #                             self.children.append(Node(self, tmp, 1))
        #                             return
        #                         else:
        #                             break
        #                     else:
        #                         self.children.append(Node(self, tmp, 1))
        #                         return
        #                 else:
        #                     tmp[i, j] = 1
        #                     if child_board:
        #                         if not self.compare_children(tmp, child_board):
        #                             self.children.append(Node(self, tmp, 2))
        #                             return
        #                         else:
        #                             break
        #                     else:
        #                         self.children.append(Node(self, tmp, 2))
        #                         return
        # print(f"Children {self.children}")
        # no more children
        self.expanded = True
        return

    # True if children states are equal
    def compare_children(self, new_child, children):
        for child in children:
            if (new_child == child).all():
                return True
        return False

