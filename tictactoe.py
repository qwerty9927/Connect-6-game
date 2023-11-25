import numpy as np
from collections import defaultdict

class Connect6:
    def __init__(self):
        self.board_size = 19
        self.win_length = 6
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1  # Player 1 starts
        self.winner = None

    def get_legal_actions(self):
        return list(zip(*np.where(self.board == 0)))

    def is_game_over(self):
        return self.winner is not None or np.all(self.board != 0)

    def move(self, action):
        if self.board[action] == 0:
            self.board[action] = self.current_player
            self.check_winner(action)
            self.current_player = 3 - self.current_player  # Switch player
        return self

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
        simulation_no = 1000  # Increase this for better results
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=1.4).parent_action

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
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

# Example usage
if __name__ == "__main__":
    game = Connect6()
    mcts = MonteCarloTreeSearchNode(game)

    while not game.is_game_over():
        if game.current_player == 1:
            action = mcts.best_action()
        else:
            print("Current board:")
            print(game.board)
            print("Legal moves:", game.get_legal_actions())
            action = tuple(map(int, input("Enter your move (x y): ").split()))
            while action not in game.get_legal_actions():
                print("Invalid move. Please choose a legal move.")
                action = tuple(map(int, input("Enter your move (x y): ").split()))

        game.move(action)

    print("Final board:")
    print(game.board)

    if game.winner is not None:
        print(f"Player {game.winner} wins!")
    else:
        print("It's a draw!")
