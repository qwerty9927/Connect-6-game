import numpy as np
import random
from collections import defaultdict
from rules import Referee

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def best_action(self):
        simulation_no = 10
        for i in range(simulation_no):
        
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
      
        return self.best_child(c_param=1.4)

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
    
    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions
    
    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node 
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    
    def n(self):
        return self._number_of_visits
    
    def best_child(self, c_param=1.4):
        # choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self.children]
        print(choices_weights)
        return self.children[np.argmax(choices_weights)]

    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.is_game_over():
            
            possible_moves = current_rollout_state.get_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()
    
    def rollout_policy(self, possible_moves):
        print(possible_moves)
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
    
class State:
    
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def get_legal_actions(self): 
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        legal_actions = []
        for i in range(19):
            for j in range(19):
                if self.board[i][j] == 0:
                    legal_actions.append([i, j])
        return legal_actions
                        


    def is_game_over(self):
        '''
        Modify according to your game or 
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        rule = Referee(self.board)
        if rule.determine() is not None:
            return True
        return False

    def game_result(self):
        '''
        Modify according to your game or 
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        # winner = None
        rule = Referee(self.board)
        winner = rule.determine()
       
        # Tie
        if winner is None:
            return 0
        else:
            # Win
            if self.player == winner:
                return 1
            # Defeat
            else:
                return -1
            
    def move(self,action):
        '''
        Modify according to your game or 
        needs. Changes the state of your 
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board 
        position is empty. If you place x in
        row 2 column 3, then it would be some 
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns 
        the new state after making a move.
        '''
        self.board[action[0]][action[1]] = self.player
        return State(self.board.copy(), self.player)

