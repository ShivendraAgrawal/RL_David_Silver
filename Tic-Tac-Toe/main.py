import json
import os
import random
from game import TicTacToe
from flask_cors import CORS
from flask import Flask, render_template, request, url_for, Response, redirect, send_from_directory

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
ticTacToe = None


def get_file(filename):
    try:
        src = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/', methods=['GET'])
def index():
    global ticTacToe
    ticTacToe = TicTacToe()
    content = get_file('tic-tac-toe.html')
    return Response(content, mimetype="text/html")

@app.route('/play_one_round', methods=['POST'])
def play_one_round():
    global ticTacToe
    if request.method == 'POST':
        button_id = request.form['button_id']
        clicked_grid = (int(button_id[0]), int(button_id[1]))

        ticTacToe.set_one_grid(clicked_grid[0], clicked_grid[1])
        solved, result = ticTacToe.is_solved()

        if solved:
            player = ticTacToe.turn if result == 1 else 0
            return Response(json.dumps({'player' : player,
                                        'solved' : True}),
                        mimetype='application/json')

        response = {'player' : ticTacToe.turn, 'solved' : False}
        ticTacToe.toggle_turn()
        return Response(json.dumps(response),
                        mimetype='application/json')

@app.route('/random_player', methods=['POST'])
def random_player_one_round():
    global ticTacToe

    button_id = request.form['button_id']
    print(button_id)
    clicked_grid = (int(button_id[0]), int(button_id[1]))

    ticTacToe.set_one_grid(clicked_grid[0], clicked_grid[1])
    solved, result = ticTacToe.is_solved()

    if solved:
        player = ticTacToe.turn if result == 1 else 0
        return Response(json.dumps({'player': player,
                                    'solved': True,
                                    'buttonID': None}),
                        mimetype='application/json')

    ticTacToe.toggle_turn()
    selected_grid = random.choice(ticTacToe.get_empty_cells())
    ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
    solved, result = ticTacToe.is_solved()

    if solved:
        player = ticTacToe.turn if result == 1 else 0
        return Response(json.dumps({'player': player,
                                    'solved': True,
                                    'buttonID': "".join([str(i) for i in selected_grid])}),
                        mimetype='application/json')

    ticTacToe.toggle_turn()

    response = {'player': ticTacToe.turn, 'solved': False,
                'buttonID' : "".join([str(i) for i in selected_grid])}


    return Response(json.dumps(response),
                    mimetype='application/json')


@app.route('/random_player_first_round_as_player_1', methods=['GET'])
def random_player_first_round():
    global ticTacToe
    selected_grid = random.choice(ticTacToe.get_empty_cells())
    ticTacToe.set_one_grid(selected_grid[0], selected_grid[1])
    ticTacToe.toggle_turn()
    return Response(json.dumps({'buttonID' : "".join(
                    [str(i) for i in selected_grid])}),
                    mimetype='application/json')

def main():
    ticTacToe = TicTacToe()

    ticTacToe.set_one_grid(0, 0)
    ticTacToe.set_one_grid(1, 0)
    ticTacToe.set_one_grid(2, 0)

    ticTacToe.print_board()
    print(ticTacToe.get_current_state())

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0')