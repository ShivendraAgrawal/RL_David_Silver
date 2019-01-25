
class TicTacToe:
    def __init__(self):
        self.empty = '-'
        self.board = [[self.empty for _ in range(3)] for _ in range(3)]
        self.turn = 1
        self.total_count = 0

    def print_board(self):
        board = """
                     {} | {} | {}
                    -----------
                     {} | {} | {}
                    -----------
                     {} | {} | {}
                """.format(*[self.board[i][j] for i in range(3) for j in range(3)])
        print(board)

    def is_solved(self):
        for row in self.board:
            if row[0] == row[1] == row[2] !=self.empty:
                return True, 1
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] !=self.empty:
                return True, 1
        if self.board[0][0] == self.board[1][1] == self.board[2][2] !=self.empty:
            return True, 1
        if self.board[0][2] == self.board[1][1] == self.board[2][0] !=self.empty:
            return True, 1
        if self.total_count == 9:
            return True, 0
        return False, None

    def set_one_grid(self, x, y):
        if self.turn == 1:
            to_set = 'X'
        else:
            to_set = 'O'
        self.board[x][y] = to_set
        self.total_count += 1

    def toggle_turn(self):
        self.turn = 2 if self.turn == 1 else 1

    def get_current_state(self):
        return tuple(tuple(x) for x in self.board)

    def get_empty_cells(self):
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.empty:
                    empty_cells.append((i, j))
        return empty_cells


