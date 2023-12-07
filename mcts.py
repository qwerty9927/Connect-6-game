import numpy as np
from collections import defaultdict
from logger import MoveLogger
import time

class Connect6:
    def __init__(self, board, player, deep):
        self.board_size = 19
        self.win_length = 6
        self.board = board
        self.current_player = player  # Player 1 starts
        self.winner = None
        self.deep = deep
        self.current_action = None

    def get_legal_actions(self):
        return list(zip(*np.where(self.board == 0)))

    def switch_player(self):
        new_player = self.current_player
        if self.deep == 0:
            new_player = 1
        elif self.deep % 2 == 0:
            new_player = 3 - self.current_player
        return new_player

    # def switch_player(self):
    #     new_player = self.current_player
    #     if self.player_moved_count == 2:
    #         new_player = 3 - self.current_player
    #         self.player_moved_count = 0
    #     self.player_moved_count += 1
    #     return new_player
    
    def is_game_over(self):
        return self.winner is not None or np.all(self.board != 0)

    def move(self, action, board, deep):
        new_state = Connect6(board, self.switch_player(), deep)
        new_state.board[action] = new_state.current_player
        new_state.check_winner(action)
        new_state.current_action = action
        return new_state
    
    def move_rollout(self, action):
        self.board[action] = self.switch_player()
        self.check_winner(action)

    def check_winner(self, last_move):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                count = 1  # Count the current move
                x, y = last_move
                while 0 <= x+i < self.board_size and 0 <= y+j < self.board_size and self.board[x+i, y+j] == self.current_player:
                    count += 1
                    x += i
                    y += j
                    if count == self.win_length:
                        self.winner = self.current_player
                        return

    def game_result(self):
        if self.winner is not None:
            return 1 if self.winner == 1 else -1
        return 0

class MonteCarloTreeSearchNode:
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
        time0 = time.time()
        logger = MoveLogger()
        playout = 0
        while(time.time() - time0) < 10:
        # for i in range(206):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward, logger)
            v.state.winner = None
            playout += 1
        print("Playout: ", playout)
        result = self.best_child(c_param=1.41)
        # logger.save_to_file()
        print(f"N: {result.n()} Q: {result.q()}")
        return result.parent_action

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand(current_node.state.deep + 1)
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

    def expand(self, deep):
        action = self._untried_actions.pop()
        next_state = self.state.move(action, self.state.board.copy(), deep)
        # print(next_state.board)
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
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    # def best_child(self, c_param=1.4, num_children=10):
    #     choices_weights = [
    #         (c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self.children
    #     ]

    #     # Sắp xếp các con theo thứ tự giảm dần của giá trị UCB
    #     sorted_children_indices = np.argsort(choices_weights)[::-1]

    #     # Chọn ra 10 con đầu tiên (hoặc ít hơn nếu có ít hơn 10 con)
    #     selected_children_indices = sorted_children_indices[:num_children]

    #     # Trả về danh sách chứa 10 node tốt nhất
    #     for i in selected_children_indices:
    #         print(self.children[i].parent_action)

    #     return self.children[np.argmax(choices_weights)]

    def rollout(self):
        rollout_state = Connect6(self.state.board.copy(), self.state.current_player, self.state.deep)
        while not rollout_state.is_game_over():
            possible_moves = rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            rollout_state.deep += 1
            rollout_state = rollout_state.move(action, rollout_state.board.copy(), rollout_state.deep)
        return rollout_state.game_result()

    def rollout_policy_index(self, possible_moves):
        return np.random.randint(len(possible_moves))
    
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result, logger):
        # logger.log(3, 3, self.state.current_player)
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result, logger)

