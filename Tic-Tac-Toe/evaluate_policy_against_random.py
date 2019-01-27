import pickle
import random

from game import TicTacToe

ticTacToe = None
policy = pickle.load(open("policy_10000000_episodes.p", "rb"))


def main(rounds):
    global ticTacToe
    wins, losses = 0, 0

    first_turn_random_count = 0
    # Running Q-Learning Q-value updates for many episodes
    for i in range(rounds):
        if i%10000 == 0:
            print("Rounds done = {}".format(i), end=" | ")
            print("Wins = {}".format(wins), end=" | ")
            print("Losses = {}".format(losses))
            wins = 0
            losses = 0
        ticTacToe = TicTacToe()
        current_state = None

        first_turn = random.choice(['random', 'computer'])
        if first_turn == 'random':
            first_turn_random_count += 1
            # Random player playing one turn
            selected_grid = random.choice(ticTacToe.get_empty_cells())
            ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
            ticTacToe.toggle_turn()

        while current_state != 'terminal':
            current_state = ticTacToe.get_current_state()
            try:
                selected_grid = policy[current_state]
                if selected_grid not in ticTacToe.get_empty_cells():
                    selected_grid = random.choice(ticTacToe.get_empty_cells())
            except:
                selected_grid = random.choice(ticTacToe.get_empty_cells())
            ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
            solved, result = ticTacToe.is_solved()
            if solved:
                if result != 0:
                    wins += 1
                break
            ticTacToe.toggle_turn()

            selected_grid = random.choice(ticTacToe.get_empty_cells())
            ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
            solved, result = ticTacToe.is_solved()
            if solved:
                if result != 0:
                    losses += 1
                break
            ticTacToe.toggle_turn()
    print("First turn by random players = {}%".format(first_turn_random_count*100/rounds))




if __name__ == "__main__":
    main(rounds = 1000000)