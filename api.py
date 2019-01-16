import datetime
import os

from flask import Flask, jsonify, abort, url_for, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
    res.append(url_for('stats_range'))
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


@app.route('/stats/range', methods=['GET'])
def stats_range():
    if request.args.get('start_date') is None or request.args.get('end_date') is None:
        return jsonify({'error': 'Bad request'}), 400
    start_date = datetime.datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

    if start_date > end_date:
        return jsonify({'error': 'End date should be after Start date'}), 400

    out = []
    while start_date <= end_date:
        if os.path.isfile(DATA_PATH + start_date.strftime("%Y-%m-%d") + '.csv'):
            print("Adding data for " + start_date.strftime("%Y-%m-%d"))
            csv_file = open(DATA_PATH + start_date.strftime("%Y-%m-%d") + '.csv', 'r')
            for row in csv_file:
                # We remove \n and split by ';'
                out.append(row.rstrip().split(';'))
        else:
            print(start_date.strftime("%Y-%m-%d") + " -> No CSV")
        start_date = start_date + datetime.timedelta(days=1)
        print(start_date.strftime("%Y-%m-%d") + " -> New start_date")
    if not out:
        return jsonify({'error': 'No data for this range'}), 404
    else:
        return jsonify(out)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': str(error)}), 404
