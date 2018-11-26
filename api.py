from flask import Flask, jsonify, abort

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello World !'})


@app.route('/stats')
def all_stats():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': 'What the fuck you are doing here ?'}), 404
