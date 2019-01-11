import random
from pprint import pprint

def epsilon_greedy(Q_values, s, epsilon):
    random_number = random.random()
    if random_number < epsilon:
        return random.choice(['left', 'right', 'up', 'down'])
    else:
        return max(Q_values[s].keys(), key = lambda a: Q_values[s][a])


def windy_action(x, y, terminal_states, action, windy_columns, n_rows, n_columns):
    '''
    The function to calculate reward and new state
    based on the action and current state

    :param x: current x location
    :param y: current y location
    :param terminal_states: List of all terminal states as tuples
    :param action: Either 'left' or 'right' or 'up' or 'down'
    :return: reward, (new_x, new_y)
    '''

    # If you are already in a terminal state you
    # can't move and would get 0 reward
    if (x, y) in terminal_states:
        return 0, (x, y)

    neighbors = {'left': (x, y - 1) if y != 0 else (x, y),
                 'right': (x, y + 1) if y != n_columns - 1 else (x, y),
                 'up': (x - 1, y) if x != 0 else (x, y),
                 'down': (x + 1, y) if x != n_rows - 1 else (x, y)}

    intended_next_state = neighbors[action]
    intended_x, intended_y = intended_next_state
    # Initialing the actual state after environmental interference
    actual_x, actual_y = intended_x, intended_y
    if y in windy_columns:
        actual_x = intended_x - windy_columns[y]
    actual_x = 0 if actual_x < 0 else actual_x

    return -1, (actual_x, actual_y)


def find_optimal_policy(Q_values, terminal_states):
    states = list(Q_values.keys())
    n_rows, n_columns = max(states, key=lambda x: x[0] + x[1])
    n_columns += 1
    n_rows += 1
    policy = [[None for _ in range(n_columns)] for _ in range(n_rows)]
    for state in states:
        best_action = max(Q_values[state].keys(), key = lambda a: Q_values[state][a])
        x, y = state
        policy[x][y] = best_action
    for (x, y) in terminal_states:
        policy[x][y] = None
    return policy


def print_prettified_policy(optimal_policy):
    prettified_optimal_policy = [[None for _ in optimal_policy[0]] for _ in optimal_policy]
    visualPolicyMap = {'left': '←', 'right': '➜', 'up': '↑', 'down': '↓', None : '∅'}
    for i in range(len(optimal_policy)):
        for j in range(len(optimal_policy[0])):
            prettified_optimal_policy[i][j] = visualPolicyMap[optimal_policy[i][j]]
    print("\nOne of the optimal policies:\n")
    for row in prettified_optimal_policy:
        print(row)


def find_path(start_state, optimal_policy, terminal_states, windy_columns):
    path = [[" " for _ in optimal_policy[0]] for _ in optimal_policy]
    current_state = start_state
    x, y = current_state
    path[x][y] = "*"
    total_reward = 0

    while current_state not in terminal_states:
        next_action = optimal_policy[x][y]

        reward, next_state = windy_action(x, y, terminal_states, next_action,
                                  windy_columns, len(path), len(path[0]))
        total_reward += reward
        current_state = next_state
        x, y = current_state
        path[x][y] = "*"
    print("\nOne of the optimal paths :\n")
    for row in path:
        print(row)
    print("\ntotal time steps taken : {}\n".format(abs(total_reward)))


def SARSA(Q_values, alpha, gamma, epsilon, terminal_states, windy_columns, n_rows, n_columns):
    current_state = (3, 0) # could be anything
    current_state = (random.randint(0, n_rows-1), random.randint(0, n_columns-1))
    current_action = epsilon_greedy(Q_values, current_state, epsilon)
    next_state, next_action = None, None
    count = 0
    while next_state not in terminal_states:
        count += 1
        current_reward, next_state = windy_action(current_state[0],
                                                  current_state[1],
                                                  terminal_states,
                                                  current_action,
                                                  windy_columns,
                                                  n_rows, n_columns)
        next_action = epsilon_greedy(Q_values, next_state, epsilon) # Q values not updated so far
        Q_values[current_state][current_action] += alpha * (current_reward + gamma
                                                            * Q_values[next_state][next_action]
                                                            - Q_values[current_state][current_action])
        current_state = next_state
        current_action = next_action
    # print("Current episode ran for {} time steps".format(count))
    return Q_values


def main(rounds):
    n_rows, n_columns = 7, 10
    gridWorld = [[(i, j) for j in range(n_columns)] for i in range(n_rows)]
    windy_columns = {3:1, 4:1, 5:1, 6:2, 7:2, 8:1}
    initial_q_value = 0.0
    terminal_states =  [(3, 7)]
    alpha = 0.5
    gamma = 1.0
    epsilon = 0.2

    Q_values = {state : {'left': initial_q_value, 'right': initial_q_value,
                 'up': initial_q_value, 'down': initial_q_value}
                for state in [state for row in gridWorld for state in row]}

    for i in range(rounds):
        Q_values = SARSA(Q_values, alpha, gamma, epsilon, terminal_states, windy_columns, n_rows, n_columns)

    # pprint(Q_values)

    optimal_policy = find_optimal_policy(Q_values, terminal_states)
    for row in optimal_policy:
        print(row)
    print_prettified_policy(optimal_policy)

    find_path((3, 0), optimal_policy, terminal_states, windy_columns)


if __name__ == "__main__":
    main(rounds = 10000)