import random

import numpy as np

from games.examples.tictactoe import TicTacToeMove, TicTacToeGameState

BOARD_SIZE = 3
SYMBOLS = {0: " ", TicTacToeGameState.x: "X", TicTacToeGameState.o: "O"}


def render(board):
    """Prints the board with 1-based row and column labels."""
    print()
    print("    " + "   ".join(str(i + 1) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print("{0}   {1}".format(i + 1, " | ".join(SYMBOLS[int(v)] for v in row)))
        if i < BOARD_SIZE - 1:
            print("   " + "-" * (BOARD_SIZE * 4 - 1))
    print()


def ask_side():
    """Asks which side the human plays, x always moves first."""
    while True:
        answer = input("Play as X (moves first) or O? [x/o, default x]: ")
        answer = answer.strip().lower()
        if answer in ("", "x"):
            return TicTacToeGameState.x
        if answer == "o":
            return TicTacToeGameState.o
        print("Please answer 'x' or 'o'.")


def ask_move(state):
    """
    Prompts for a move as 'row col' until a legal one is entered.
    Returns None if the player quits.
    """
    while True:
        answer = input("Your move (row col, or q to quit): ").strip().lower()
        if answer in ("q", "quit"):
            return None
        try:
            row, col = map(int, answer.split())
        except ValueError:
            print("Enter two numbers separated by a space, e.g. '2 3'.")
            continue
        move = TicTacToeMove(row - 1, col - 1, state.next_to_move)
        if state.is_move_legal(move):
            return move
        print("Illegal move, pick an empty cell on the board.")


def random_policy(state):
    """Picks uniformly among the legal moves."""
    return random.choice(state.get_legal_actions())


def play():
    human = ask_side()
    state = TicTacToeGameState(np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int))
    render(state.board)

    while not state.is_game_over():
        if state.next_to_move == human:
            move = ask_move(state)
            if move is None:
                print("Bye!")
                return
        else:
            move = random_policy(state)
            print("Random policy plays {0} {1}".format(
                move.x_coordinate + 1, move.y_coordinate + 1
            ))
        state = state.move(move)
        render(state.board)

    result = state.game_result
    if result == 0:
        print("It's a draw.")
    elif result == human:
        print("You win!")
    else:
        print("The random policy wins.")


if __name__ == "__main__":
    try:
        play()
    except (EOFError, KeyboardInterrupt):
        print("\nBye!")
