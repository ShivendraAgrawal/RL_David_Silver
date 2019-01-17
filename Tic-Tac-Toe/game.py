
class TicTacToe:
    def __init__(self):
        self.empty = '-'
        self.board = [[self.empty for _ in range(3)] for _ in range(3)]
        self.turn = 1

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
                return True
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] !=self.empty:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] !=self.empty:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] !=self.empty:
            return True
        return False

    def set_one_grid(self, x, y):
        if self.turn == 1:
            to_set = 'X'
        else:
            to_set = 'O'
        self.board[x][y] = to_set

    def toggle_turn(self):
        self.turn = 2 if self.turn == 1 else 1




