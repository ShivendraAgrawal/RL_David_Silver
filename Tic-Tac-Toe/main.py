import os

from game import TicTacToe
from flask_cors import CORS
from flask import Flask, render_template, request, url_for, Response, redirect, send_from_directory

app = Flask(__name__, static_url_path='')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/', methods=['GET'])
def index():
    content = get_file('tic-tac-toe.html')
    return Response(content, mimetype="text/html")


def main():
    ticTacToe = TicTacToe()

    ticTacToe.set_one_grid(0, 0)
    ticTacToe.set_one_grid(1, 0)
    ticTacToe.set_one_grid(2, 0)

    ticTacToe.print_board()
    print(ticTacToe.is_solved())

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0')