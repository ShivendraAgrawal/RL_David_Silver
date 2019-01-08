
def action(x,y, terminal_states, direction):
    '''
    The function to calculate reward and new state
    based on the action and current state

    :param x: current x location
    :param y: current y location
    :param terminal_states: List of all terminal states as tuples
    :param direction: Either 'left' or 'right' or 'up' or 'down'
    :return: reward, (new_x, new_y)
    '''

    # If you are already in a terminal state you
    # can't move and would get 0 reward
    if (x, y) in terminal_states:
        return 0, (x, y)

    new_x, new_y = x, y
    if direction == 'left':
        if y == 0:
            new_y = 0
        else:
            new_y = y - 1
    if direction == 'right':
        if y == 3:
            new_y = 3
        else:
            new_y = y + 1
    if direction == 'up':
        if x == 0:
            new_x = 0
        else:
            new_x = x - 1
    if direction == 'down':
        if x == 3:
            new_x = 3
        else:
            new_x = x + 1

    return -1, (new_x, new_y)


def find_optimal_policy(v_grid, terminal_states):
    policy = [[None for _ in range(len(v_grid[0]))] for _ in range(len(v_grid))]

    for i in range(len(v_grid)):
        for j in range(len(v_grid[0])):
            neighbors = {'←': (i, j-1) if j != 0 else (i, j),
                         '➜': (i, j+1) if j != len(v_grid[0])-1 else (i, j),
                         '↑': (i-1, j) if i != 0 else (i, j),
                         '↓': (i+1, j) if i != len(v_grid)-1 else (i, j)}
            best_action = max(neighbors.keys(),
                              key=lambda x: -1 + v_grid[neighbors[x][0]][neighbors[x][1]]) # -1 is the reward
            policy[i][j] = best_action
    for (x, y) in terminal_states:
        policy[x][y] = '∅'

    print("\nOne of the optimal policies:\n")
    for row in policy:
        print(row)
    return policy


def main(rounds):
    v_grid = [[0, 0, 0, 0] for _ in range(4)] # Initial value function for all states
    policy_prob = 0.25 # Probability for choosing an action -> Not an optimal policy
    terminal_states = [(0, 0), (3, 3)]

    for k in range(rounds):
        v_grid_new = [[None for _ in range(len(v_grid[0]))] for _ in range(len(v_grid))]
        for i in range(len(v_grid)):
            for j in range(len(v_grid[0])):

                # Calculating the rewards for all possible actions from state (i, j)
                reward_left, (new_x_left, new_y_left) = action(i, j, terminal_states, 'left')
                reward_right, (new_x_right, new_y_right) = action(i, j, terminal_states, 'right')
                reward_up, (new_x_up, new_y_up) = action(i, j, terminal_states, 'up')
                reward_down, (new_x_down, new_y_down) = action(i, j, terminal_states, 'down')

                # Averaging rewards from all actions
                v_grid_new[i][j] = policy_prob * (reward_left + v_grid[new_x_left][new_y_left] +
                                                  reward_right + v_grid[new_x_right][new_y_right] +
                                                  reward_up + v_grid[new_x_up][new_y_up] +
                                                  reward_down + v_grid[new_x_down][new_y_down])
        # Updating the Value function for all states
        v_grid = v_grid_new.copy()

        print("\nRound {}".format(k+1))
        for row in v_grid:
            my_rounded_row = [round(elem, 1) for elem in row]
            print(my_rounded_row)

    find_optimal_policy(v_grid, terminal_states)

if __name__ == "__main__":
    main(rounds = 120)
