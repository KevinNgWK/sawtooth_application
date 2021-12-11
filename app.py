import sys
import os
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
# URL = 'tcp://172.19.174.169:4004'
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