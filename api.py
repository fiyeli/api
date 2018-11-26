from flask import Flask, jsonify, abort

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello World !'})


@app.route('/stats', methods=['GET'])
def stats():
    abort(404)


@app.route('/stats/today', methods=['GET'])
def stats_today():
    abort(404)


@app.route('/stats/<date>', methods=['GET'])
def stats_day(date):
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': str(error)}), 404
