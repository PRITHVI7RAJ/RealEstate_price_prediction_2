from flask import Flask, request, jsonify
import util

app = Flask(__name__)


def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@app.route('/')
def home():
    return "Home Price Prediction API is running."


@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    return add_cors_headers(response)


@app.route('/predict_home_price', methods=['POST', 'OPTIONS'])
def predict_home_price():
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({'status': 'ok'}))

    data = request.get_json(silent=True) or request.form

    total_sqft = float(data['total_sqft'])
    location = data['location']
    bhk = int(data['bhk'])
    bath = int(data['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })

    return add_cors_headers(response)


if  __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction")
    util.load_saved_artifacts()
    app.run()
