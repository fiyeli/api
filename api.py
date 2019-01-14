import datetime
import os

from flask import Flask, jsonify, abort, url_for

app = Flask(__name__)
DATA_PATH = os.environ.get('DATA_PATH', '../fiyeli/data/')


@app.route('/', methods=['GET'])
def hello_world():
    url = [url_for('stats')]
    return jsonify({'urls': url})


@app.route('/stats/', methods=['GET'])
def stats():
    res = []
    for file in os.listdir(DATA_PATH):
        res.append(url_for('stats_day', user_input=file.strip('.csv')))
    return jsonify({'uris': res})


@app.route('/stats/today', methods=['GET'])
def stats_today():
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    if os.path.isfile(DATA_PATH + day + '.csv'):
        return stats_day(day)
    else:
        return jsonify({'message': 'No stats generated yet, please come back later'}), 404


@app.route('/stats/<user_input>', methods=['GET'])
def stats_day(user_input):
    try:
        day_time = datetime.datetime.strptime(user_input, '%Y-%m-%d')
        day = day_time.strftime("%Y-%m-%d")
    except ValueError as e:
        return jsonify({'message': 'Invalid date. Expected format YYYY-MM-DD'}), 400
    if not os.path.isfile(DATA_PATH + str(day) + '.csv'):
        return jsonify({'message': 'No stats for this date'}), 404
    else:
        out = []
        csv_file = open(DATA_PATH + str(day) + '.csv', 'r')
        for row in csv_file:
            # We remove \n and split by ';'
            out.append(row.rstrip().split(';'))
        return jsonify(out)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': str(error)}), 404
