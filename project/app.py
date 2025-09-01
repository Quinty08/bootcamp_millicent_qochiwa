# app.py
from flask import Flask, request, jsonify
from src.utils import predict, run_full_analysis
import traceback

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok", "service": "model-api"})

@app.route("/predict", methods=["POST"])
def predict_post():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON received"}), 400
        # Accept either {"features": {...}} or a list/dict directly
        if "features" in data:
            payload = data["features"]
        else:
            payload = data
        preds = predict(payload)
        return jsonify({"status": "success", "result": preds})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/predict/<param1>", methods=["GET"])
@app.route("/predict/<param1>/<param2>", methods=["GET"])
def predict_get(param1, param2=None):
    # Example: parse params into a single-feature input. Adapt to your model schema.
    try:
        # Convert params into numeric if possible
        try:
            val1 = float(param1)
        except:
            val1 = param1
        payload = {"feat1": val1}
        if param2 is not None:
            try:
                val2 = float(param2)
            except:
                val2 = param2
            payload["feat2"] = val2
        preds = predict(payload)
        return jsonify({"status": "success", "result": preds})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/run_full_analysis", methods=["GET"])
def run_full():
    try:
        force = request.args.get("force", "false").lower() == "true"
        summary = run_full_analysis(force_retrain=force)
        return jsonify({"status": "success", "summary": summary})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # For local dev only. For production use Gunicorn or uWSGI.
    app.run(host="0.0.0.0", port=5000, debug=True)
