import os
from io import BytesIO

from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

from model import load_model

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "model", "model.joblib")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

_model = load_model(MODEL_PATH)


@app.get("/")
def root():
    return jsonify({"ok": True, "service": "ai-disease-backend", "model_loaded": _model is not None})


@app.post("/predict-image")
def predict_image():
    global _model
    if _model is None:
        return (
            jsonify({
                "ok": False,
                "error": "Model not loaded.",
                "hint": "Train a model with backend/train.py and place it at backend/model/model.joblib or deploy an image with a pre-trained model.",
            }),
            503,
        )

    if "file" not in request.files:
        return jsonify({"ok": False, "error": "Missing file in form-data under key 'file'"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"ok": False, "error": "Empty filename"}), 400

    try:
        img = Image.open(file.stream)
    except Exception as e:
        return jsonify({"ok": False, "error": f"Unable to open image: {e}"}), 400

    try:
        label, probs = _model.predict(img)
        return jsonify({"ok": True, "label": label, "scores": probs})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    # Development server (do not use in production)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
