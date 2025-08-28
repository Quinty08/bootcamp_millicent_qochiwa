# app.py
from flask import Flask, request, jsonify, send_file, abort
import io, matplotlib.pyplot as plt
from src.utils import load_model, predict_model
import numpy as np

app = Flask(__name__)
MODEL_PATH = 'model/model.pkl'

# Load model at startup
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    model = None
    print("Warning: model not loaded on startup:", e)

@app.route('/predict', methods=['POST'])
def predict_post():
    if model is None:
        return jsonify({'error': 'Model not available on server'}), 500
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    features = data.get('features')
    if features is None:
        return jsonify({'error': 'Request must include "features" list'}), 400
    try:
        # accept list or nested lists
        arr = np.array(features)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        preds = model.predict(arr).tolist()
        return jsonify({'predictions': preds})
    except Exception as e:
        return jsonify({'error': f'Error during prediction: {str(e)}'}), 400

@app.route('/predict/<float:input1>', methods=['GET'])
def predict_one(input1):
    if model is None:
        return jsonify({'error': 'Model not available on server'}), 500
    try:
        pred = model.predict([[input1]]).tolist()
        return jsonify({'prediction': pred})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict/<float:input1>/<float:input2>', methods=['GET'])
def predict_two(input1, input2):
    if model is None:
        return jsonify({'error': 'Model not available on server'}), 500
    try:
        pred = model.predict([[input1, input2]]).tolist()
        return jsonify({'prediction': pred})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/plot', methods=['GET'])
def plot_endpoint():
    # produce a simple chart and return PNG bytes
    fig, ax = plt.subplots()
    ax.plot([0,1,2,3], [0,1,4,9])
    ax.set_title('Example Plot')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return send_file(buf, mimetype='image/png',
                     attachment_filename='plot.png',
                     as_attachment=False)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
