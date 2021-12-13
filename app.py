import sys
import os
import getpass
import argparse
import pkg_resources
from flask import Flask, jsonify, request, abort

from src.handler import XoTransactionHandler

from sawtooth_sdk.processor.core import TransactionProcessor
from src.xo_client import XoClient
from src.xo_exceptions import XoException

DISTRIBUTION_NAME = 'sawtooth-xo'

AUTH_USER = None
AUTH_PASSWORD = None
URL = 'http://localhost:8008'

app = Flask(__name__)


def create_error_response(message, status_code=400):
    resp = jsonify(error=message)
    resp.status_code = status_code
    return resp


@app.route('/list')
def list_games():
    client = XoClient(base_url=URL, keyfile=None)

    game_list = [
        game.split(',')
        for games in client.list(auth_user=AUTH_USER,
                                 auth_password=AUTH_PASSWORD)
        for game in games.decode().split('|')
    ]

    if game_list is not None:
        return jsonify(game_list)
    else:
        raise XoException("Could not retrieve game listing.")


@app.route('/show', methods=['POST'])
def show_game():
    name = request.get_json()['name']
    client = XoClient(base_url=URL, keyfile=None)

    data = client.show(name, auth_user=AUTH_USER, auth_password=AUTH_PASSWORD)

    if data is not None:
        board_str, game_state, player1, player2 = {
            name: (board, state, player_1, player_2)
            for name, board, state, player_1, player_2 in [
                game.split(',')
                for game in data.decode().split('|')
            ]
        }[name]
        
        board = list(board_str.replace("-", " "))
        ret = {
            'game': name,
            'player 1': player1[:6],
            'player 2': player2[:6],
            'state': game_state,
            'board': [board[:3], board[3:6], board[6:9]]
        }
        return jsonify(ret)
    else:
        raise XoException("Game not found: {}".format(name))


@app.route('/create', methods=['POST'])
def create_game():
    req = request.get_json()
    name, username = None, None
    if 'name' in req:
        name = req['name']
    if 'username' in req:
        username = req['username']
    keyfile = _get_keyfile(username)
    print(keyfile)

    client = XoClient(base_url=URL, keyfile=keyfile)

    response = client.create(name, auth_user=AUTH_USER, auth_password=AUTH_PASSWORD)
    return jsonify(response)


@app.route('/take', methods=['POST'])
def take_position():
    req = request.get_json()
    name = req['name'] 
    space = req['space']
    username = req['username']

    keyfile = _get_keyfile(username)

    client = XoClient(base_url=URL, keyfile=keyfile)

    response = client.take(name, space, auth_user=AUTH_USER, auth_password=AUTH_PASSWORD)
    return jsonify(response)


@app.route('/delete', methods=['POST'])
def delete_game():
    req = request.get_json()
    name = req['name']
    username = req['username']

    keyfile = _get_keyfile(username)

    client = XoClient(base_url=URL, keyfile=keyfile)

    response = client.delete(name, auth_user=AUTH_USER, auth_password=AUTH_PASSWORD)
    return jsonify(response)



def _get_keyfile(username):
    username = getpass.getuser() if username is None else username
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, username)


if __name__ == '__main__':
    port = os.getenv('PORT') or 5000
    app.run(debug=False, host='0.0.0.0', port=int(port))
    try:
        processor = TransactionProcessor(url=URL)
        handler = XoTransactionHandler()
        processor.add_handler(handler)
        processor.start()
    except os.error as err:
        print(err)