import numpy as np
from collections import defaultdict
from games.examples.tictactoe import TicTacToeGameState, TicTacToeMove

#Assume we get reward +1 if we win, 0 if draw and -1 if loose

class TreeNode():
    def __init__(self, state : TicTacToeGameState, parent=None):
        
        self.state = state
        self.parent = parent
        self.n_visits = 0
        
        untried_actions = self.state.get_legal_actions()

        #sum of wins +1, draws 0 and losses -1
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
    



if __name__ == "__main__":

    state = np.zeros((3,3))
    initial_board_state = TicTacToeGameState(state = state, next_to_move=1)

    root = TreeNode(state = initial_board_state)
    print(root)

    root.rollout()
