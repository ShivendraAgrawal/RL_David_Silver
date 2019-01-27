import time
from pprint import pprint
from game import TicTacToe
import random, pickle
from collections import defaultdict

ticTacToe = None
wins = 0
losses = 0

def epsilon_greedy(Q_values, s, actions_per_state, epsilon):
    global ticTacToe

    if s not in Q_values:
        Q_values[s] = actions_per_state.copy()

    random_number = random.random()
    # With ε probability choose any action
    if random_number < epsilon:
        return random.choice(ticTacToe.get_empty_cells())
    # With 1 - ε probability pick the action greedily
    else:
        try:
            return max(ticTacToe.get_empty_cells(), key = lambda a: Q_values[s][a])
        except ValueError:
            return None

def epsilon_greedy_for_opposition(Q_values, s, actions_per_state, epsilon):
    global ticTacToe

    if s not in Q_values:
        Q_values[s] = actions_per_state.copy()

    random_number = random.random()
    # With ε probability choose any action
    if random_number < epsilon:
        return random.choice(ticTacToe.get_empty_cells())
    # With 1 - ε probability pick the action greedily
    else:
        try:
            return min(ticTacToe.get_empty_cells(), key = lambda a: Q_values[s][a])
        except ValueError:
            return None

def take_action_with_Q_opposition(current_action, Q_values, actions_per_state, epsilon):
    global ticTacToe
    ticTacToe.set_one_grid(current_action[0], current_action[1])
    solved, result = ticTacToe.is_solved()
    if solved:
        reward = result
        return reward, 'terminal'
    ticTacToe.toggle_turn()

    # Q opposition player playing one turn
    selected_grid = epsilon_greedy_for_opposition(Q_values,
                                                  ticTacToe.get_current_state(),
                                                  actions_per_state,
                                                  epsilon)
    if selected_grid not in ticTacToe.get_empty_cells():
        selected_grid = random.choice(ticTacToe.get_empty_cells())

    ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
    solved, result = ticTacToe.is_solved()
    if solved:
        reward = -1 * result
        return reward, 'terminal'
    ticTacToe.toggle_turn()

    return 0, ticTacToe.get_current_state()

def take_action_with_random_opposition(current_action):
    global ticTacToe
    ticTacToe.set_one_grid(current_action[0], current_action[1])
    solved, result = ticTacToe.is_solved()
    if solved:
        reward = result
        return reward, 'terminal'
    ticTacToe.toggle_turn()

    # Random player playing one turn
    selected_grid = random.choice(ticTacToe.get_empty_cells())
    ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
    solved, result = ticTacToe.is_solved()
    if solved:
        reward = -1 * result
        return reward, 'terminal'
    ticTacToe.toggle_turn()

    return 0, ticTacToe.get_current_state()



def Q_Learning(Q_values, alpha, gamma, epsilon, actions_per_state):
    global ticTacToe
    global wins
    global losses
    # Randomly pick a state to start the episode
    current_state = ticTacToe.get_current_state()
    next_state, current_action = None, None

    # A variable to count the time steps in the current episode
    count = 0
    # Repeat for each time step of the episode till the episode ends
    while next_state != 'terminal':
        count += 1
        # Pick the action using ε-greedy strategy
        current_action = epsilon_greedy(Q_values, current_state, actions_per_state, epsilon)

        # Take the action either with Q opposition or random opposition
        # current_reward, next_state = take_action_with_random_opposition(current_action)
        current_reward, next_state = take_action_with_Q_opposition(current_action,
                                                                   Q_values,
                                                                   actions_per_state,
                                                                   epsilon)

        if current_reward == 1:
            wins += 1
        elif current_reward == -1:
            losses += 1

        # Use the Q values to greedily find the next action for
        # the state you would reach after the wind interference
        # Note that 'epsilon_greedy' policy was converted to a
        # greedy one by setting 'epsilon = 0'
        next_action = epsilon_greedy(Q_values, next_state, actions_per_state, epsilon = 0) # Q values not updated so far

        # Update the Q values after getting better estimates after 1-step look-ahead using Q-Learning
        Q_values[current_state][current_action] += alpha * (current_reward + gamma
                                                            * Q_values[next_state][next_action]
                                                            - Q_values[current_state][current_action])
        current_state = next_state

    # Uncomment if you want to see how long each episode ran for,
    # expect to see an exponential decrease in the time steps per
    # episode as you improve your Q values
    # print("Current episode ran for {} time steps".format(count))
    return Q_values

def find_optimal_policy(Q_values):
    '''
    After the Q values have converged, a function to
    greedily find the optimal policy at each state
    :param Q_values: A dict of dict with 1st key as state
                    and 2nd as action and value as the Q value
    :return: An optimal policy for each state in the grid world
    '''
    policy = {}
    for state in Q_values:
        best_action = max(Q_values[state].keys(), key = lambda a: Q_values[state][a])
        policy[state] = best_action
    policy['terminal'] = None
    return policy

def main(rounds):
    global ticTacToe
    global wins
    global losses

    initial_q_value = 0.0
    alpha = 0.5 # Step size
    gamma = 1.0 # Discount factor
    epsilon = 0.2 # Exploration rate

    actions = [(i, j) for i in range(3) for j in range(3)]
    actions_per_state = {a : initial_q_value for a in actions}

    Q_values = {'terminal' : actions_per_state.copy()}
    Q_values['terminal'][None] = 0.0

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

        first_turn = random.choice(['random', 'computer'])
        if first_turn == 'random':
            first_turn_random_count += 1
            # Random player playing one turn
            # Q opposition player playing one turn
            selected_grid = epsilon_greedy_for_opposition(Q_values,
                                                          ticTacToe.get_current_state(),
                                                          actions_per_state,
                                                          epsilon)
            if selected_grid not in ticTacToe.get_empty_cells():
                selected_grid = random.choice(ticTacToe.get_empty_cells())
            ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
            ticTacToe.toggle_turn()

        Q_values = Q_Learning(Q_values, alpha, gamma,
                              epsilon, actions_per_state)


    # pprint(Q_values)
    policy = find_optimal_policy(Q_values)
    print("First turn by random players = {}%".format(first_turn_random_count*100/rounds))
    filename = "Q_values_{}_episodes.p".format(rounds)
    pickle.dump(Q_values, open(filename, "wb"))
    filename = "policy_{}_episodes.p".format(rounds)
    pickle.dump(policy, open(filename, "wb"))

if __name__ == "__main__":
    start_time = time.time()
    main(rounds = 1000000)
    print("Time taken = {}".format(time.time() - start_time))

    # 1000000 takes ~ 118 seconds