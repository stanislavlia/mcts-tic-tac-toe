import numpy as np
from collections import defaultdict
from games.examples.tictactoe import TicTacToeGameState, TicTacToeMove

#Assume we get reward +1 if we win, 0 if draw and -1 if loose

class TreeNode():
    def __init__(self, state : TicTacToeGameState, parent=None):
        
        self.state = state
        self.parent = parent
        self.n_visits = 0
        
        self.children = []

        self.untried_actions = self.state.get_legal_actions()

        #value from viewpoint of player who moved into this node
        self.value = 0

    def __str__(self):
        symbols = {0: " ", TicTacToeGameState.x: "X", TicTacToeGameState.o: "O"}
        rows = [
            " | ".join(symbols[int(cell)] for cell in row)
            for row in self.state.board
        ]
        separator = "\n" + "-" * (self.state.board_size * 4 - 1) + "\n"
        return separator.join(rows)

    def is_terminal(self):
        return self.state.is_game_over()
    
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def rollout_policy(self, legal_moves):
        #randomly selects a legal move
        return np.random.choice(legal_moves)
    

    def rollout(self):
        """Returns outcome of rollout"""

        current_state = self.state
        while not current_state.is_game_over():
            #Rollout policy chooses action for both players until game terminates
            action = self.rollout_policy(current_state.get_legal_actions())            
            current_state = current_state.move(action)

            print("GameState: ")
            print(TreeNode(current_state))

        print("Final result: ", current_state.game_result)
        return current_state.game_result
    
    def backup(self, result):
        """Backpropogate outcome up and increment n_visits"""
        self.n_visits += 1
        self.value += result * -self.state.next_to_move #multiply by who moves to correctly distribute results (so we learn values for both players)

        if self.parent:
            #call backup method for parent node
            self.parent.backup(result)
    


class MonteCarloTreeSearch():
    def __init__(self, node: TreeNode):

        self.node : TreeNode = node

    def select_action(self):
        pass

    @staticmethod
    def _ucb_score(val, n_visits, t, c):
        """Computes UCB-1 score. This score is used to select action
        while balancing between exploitation and exploration"""

        if n_visits == 0:
            return float("inf")
        exploration_term = np.sqrt(np.log(t) / n_visits)
        avg_val = val / n_visits
        return avg_val + c * exploration_term
    


if __name__ == "__main__":

    state = np.zeros((3,3))
    initial_board_state = TicTacToeGameState(state = state, next_to_move=1)

    root = TreeNode(state = initial_board_state)
    print(root)

    root.rollout()
