import random
from pprint import pprint

def epsilon_greedy(Q_values, s, epsilon):
    '''
    Given the Q values, a func to select the action
    based on ε-greedy
    :param Q_values: A dict of dict with 1st key as state
                    and 2nd as action and value as the Q value
    :param s: state (represented as (x, y) tuple)
    :param epsilon: Value of epsilon as a float
    :return: An action from ['left', 'right', 'up', 'down']
    '''
    random_number = random.random()
    # With ε probability choose any action
    if random_number < epsilon:
        return random.choice(['left', 'right', 'up', 'down'])
    # With 1 - ε probability pick the action greedily
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
    :param windy_columns: A dict with windy column index as key
                          and value as wind value
    :param n_rows: Number of rows in the grid world
    :param n_columns: Number of columns in the grid world
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

    # If you start from a windy column,
    # get pushed by the wind value in -x direction
    if y in windy_columns:
        actual_x = intended_x - windy_columns[y]
    # If you are at the 'ceiling', you can't move further upwards
    actual_x = 0 if actual_x < 0 else actual_x

    return -1, (actual_x, actual_y)


def find_optimal_policy(Q_values, terminal_states):
    '''
    After the Q values have converged, a function to
    greedily find the optimal policy at each state
    :param Q_values: A dict of dict with 1st key as state
                    and 2nd as action and value as the Q value
    :param terminal_states: List of all terminal states as tuples
    :return: An optimal policy for each state in the grid world
    '''
    states = list(Q_values.keys())
    n_rows, n_columns = max(states, key=lambda x: x[0] + x[1])
    n_columns += 1
    n_rows += 1

    # Initialize a grid world like 2d list of list to store the policies
    policy = [[None for _ in range(n_columns)] for _ in range(n_rows)]
    for state in states:
        best_action = max(Q_values[state].keys(), key = lambda a: Q_values[state][a])
        x, y = state
        policy[x][y] = best_action
    # Assign None to terminal states as all policies are equally good
    for (x, y) in terminal_states:
        policy[x][y] = None
    return policy

# A function to print a 2d matrix neatly
def print_matrix(matrix):
    n_rows = len(matrix)
    n_columns = len(matrix[0])
    print("  ", end=" ")
    for i in range(n_columns):
        print(i, end=" ")
    print("\n")
    for i in range(n_rows):
        for j in range(n_columns):
            to_print = "-"
            if j == 0:
                print(i, end="  ")
            if matrix[i][j] != " ":
                to_print = matrix[i][j]
            print(to_print, end=" ")
        print("")


def print_prettified_policy(optimal_policy):
    '''
    A func to replace actions with arrows for visual prettiness
    :param optimal_policy: An optimal policy for each state in the grid world
    :return: A prettified optimal policy as 2d list of list
    '''
    prettified_optimal_policy = [[None for _ in optimal_policy[0]] for _ in optimal_policy]
    visualPolicyMap = {'left': '←', 'right': '➜', 'up': '↑', 'down': '↓', None : '∅'}
    for i in range(len(optimal_policy)):
        for j in range(len(optimal_policy[0])):
            prettified_optimal_policy[i][j] = visualPolicyMap[optimal_policy[i][j]]
    print("\nOne of the optimal policies:\n")
    print_matrix(prettified_optimal_policy)


def find_path(start_state, optimal_policy, terminal_states, windy_columns):
    '''
    A function to utilize the optimal policy to
    depict a path taken to a terminal state
    :param start_state: A start state to start the path
    :param optimal_policy: An optimal policy for each state in the grid world
    :param terminal_states: List of all terminal states as tuples
    :param windy_columns: A dict with windy column index as key
                          and value as wind value
    :return: None (just prints the path taken in the grid world)
    '''
    path = [[" " for _ in optimal_policy[0]] for _ in optimal_policy]
    current_state = start_state
    x, y = current_state
    path[x][y] = "*"
    total_reward = 0

    # Repeat while you don't reach a terminal state
    while current_state not in terminal_states:
        # Select the best action prescribed by the optimal Q values
        next_action = optimal_policy[x][y]

        # find the final state after environmental interference
        reward, next_state = windy_action(x, y, terminal_states, next_action,
                                  windy_columns, len(path), len(path[0]))
        total_reward += reward
        current_state = next_state
        x, y = current_state
        # Mark the state as a part of the path
        path[x][y] = "*"
    print("\nOne of the optimal paths :\n")
    print_matrix(path)
    print("\ntotal time steps taken : {}\n".format(abs(total_reward)))


def Q_Learning(Q_values, alpha, gamma, epsilon, terminal_states, windy_columns, n_rows, n_columns):
    '''
    The function implementing the Q-Learning algorithm for
    updating Q values each time step for a single episode
    :param Q_values: A dict of dict with 1st key as state
                    and 2nd as action and value as the Q value
    :param alpha: The step size as a float
    :param gamma: The discount factor as a float
    :param epsilon: The exploration rate as a float
    :param terminal_states: List of all terminal states as tuples
    :param windy_columns: A dict with windy column index as key
                          and value as wind value
    :param n_rows: Number of rows in the grid world
    :param n_columns: Number of columns in the grid world
    :return:
    '''

    # Randomly pick a state to start the episode
    current_state = (random.randint(0, n_rows-1), random.randint(0, n_columns-1))
    next_state, current_action = None, None

    # A variable to count the time steps in the current episode
    count = 0
    # Repeat for each time step of the episode till the episode ends
    while next_state not in terminal_states:
        count += 1
        # Pick the action using ε-greedy strategy
        current_action = epsilon_greedy(Q_values, current_state, epsilon)

        # Take the action with wind interference
        current_reward, next_state = windy_action(current_state[0],
                                                  current_state[1],
                                                  terminal_states,
                                                  current_action,
                                                  windy_columns,
                                                  n_rows, n_columns)
        # Use the Q values to greedily find the next action for
        # the state you would reach after the wind interference
        # Note that 'epsilon_greedy' policy was converted to a
        # greedy one by setting 'epsilon = 0'
        next_action = epsilon_greedy(Q_values, next_state, epsilon = 0) # Q values not updated so far

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


def main(rounds):
    '''
    A wrapper function to initialize the grid world and
    run Q-Learning updates many times
    :param rounds: Number of episodes we want to run Q-Learning for
    :return: None (Prints all the results)
    '''

    # Initialize the grid world, Q-values and the parameters for Q-Learning
    n_rows, n_columns = 7, 10
    # A grid world with values as a tuple representing the state at each location
    gridWorld = [[(i, j) for j in range(n_columns)] for i in range(n_rows)]
    # Keys represent the columns with wind and values represent the wind intensity
    windy_columns = {3:1, 4:1, 5:1, 6:2, 7:2, 8:1}
    # Initializing all Q values as 0
    initial_q_value = 0.0
    terminal_states =  [(3, 7)]

    alpha = 0.5 # Step size
    gamma = 1.0 # Discount factor
    epsilon = 0.2 # Exploration rate

    # A dict of dict with 1st key as state and 2nd as action and value as the Q value
    Q_values = {state : {'left': initial_q_value, 'right': initial_q_value,
                 'up': initial_q_value, 'down': initial_q_value}
                for state in [state for row in gridWorld for state in row]}

    # Running Q-Learning Q-value updates for many episodes
    for i in range(rounds):
        Q_values = Q_Learning(Q_values, alpha, gamma, epsilon,
                         terminal_states, windy_columns, n_rows, n_columns)

    # Uncomment to checkout the optimal Q-values
    # pprint(Q_values)

    # Greedily find the optimal policy from the optimal Q-values
    optimal_policy = find_optimal_policy(Q_values, terminal_states)

    print_prettified_policy(optimal_policy)

    # Tracing the shortest path using the optimal policy from (3, 0)
    # to a terminal state
    find_path((3, 0), optimal_policy, terminal_states, windy_columns)


if __name__ == "__main__":
    # NOTE: Sometimes we don't find the optimal policy so it may
    # take more than 15 steps. In that case just re-run the code
    # till you get a path with 15 steps. And sometimes we get a
    # policy which has a cycle that we can't escape and the code
    # doesn't terminate, in that case again re-run the code

    # Observation: Q-Learning converges significantly faster than SARSA(0)
    main(rounds = 1000)