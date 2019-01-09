from pprint import pprint

def epsilon_greedy(Q_values, s, epsilon):
    pass



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
    if intended_y in windy_columns:
        actual_x = intended_x - windy_columns[intended_y]

    return -1, (actual_x, actual_y)



def main(n_rows, n_columns):
    gridWorld = [[(i, j) for j in range(n_columns)] for i in range(n_rows)]
    windy_columns = {3:1, 4:1, 5:1, 6:2, 7:2, 8:1}
    initial_q_value = 0.0
    Q_values = {state : {'left': initial_q_value, 'right': initial_q_value,
                 'up': initial_q_value, 'down': initial_q_value}
                for state in [state for row in gridWorld for state in row]}
    pprint(Q_values)

    print(windy_action(3, 3, [(3, 7)], 'right', windy_columns, n_rows, n_columns))

if __name__ == "__main__":
    main(7, 10)