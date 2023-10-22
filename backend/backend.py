from flask import Flask, jsonify, request
from model import LSTMModel
import json

app = Flask(__name__)

@app.route('/api/get_prediction/<ticker>', methods=['GET'])
def get_data(ticker):
    lstm = LSTMModel()
    data = lstm.get_prediction(ticker)
    predicted = data[0]
    reality = data[1]
    print("predicted:", predicted)
    print("reality:", reality)
    threshold_ceil_diff = 1.5

    avg_predicted = 0
    avg_reality = 0
    for predict in predicted:
        avg_predicted += predict
    
    for reality in reality:
        avg_reality += reality
    
    avg_predicted /= 3
    avg_reality /= 3
    result = ""

    if avg_reality - avg_predicted > threshold_ceil_diff:
        result = "sell"
    elif avg_reality - avg_predicted >= -1.0:
        result = "hold"
    else:
        result = "buy"

    return json.dumps({ "result": result })

@app.route('/')
def index():
    return jsonify({'name': 'NaN',
                    'email': 'NaN'})

if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)