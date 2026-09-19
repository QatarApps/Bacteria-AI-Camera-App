import base64
import io
from pathlib import Path
from PIL import Image
import numpy as np
import torch
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "bacteria_classifier_torchscript.pt"
LABELS_PATH = BASE_DIR / "bacteria_labels.txt"
IMAGE_SIZE = 80
TARGETS = {"Pseudomonas_aeruginosa", "Staphylococcus_aureus"}

# Load labels
labels = [x.strip() for x in LABELS_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]

# Load TorchScript model
model = torch.jit.load(str(MODEL_PATH), map_location="cpu")
model.eval()


def preprocess_pil(image: Image.Image) -> torch.Tensor:
    # Convert image to RGB
    img = image.convert("RGB")
    # Resize to IMAGE_SIZE x IMAGE_SIZE
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.BILINEAR)
    arr = np.array(img, dtype=np.float32)
    # Permute to (C, H, W) and scale to [0, 1]
    x = torch.from_numpy(arr).permute(2, 0, 1) / 255.0
    # Normalize to [-1, 1] matching training pipeline: (x - 0.5) / 0.5
    x = (x - 0.5) / 0.5
    return x.unsqueeze(0)


@app.route("/")
def index():
    return render_template("index.html", labels=labels, targets=list(TARGETS))


@app.route("/health")
def health():
    return jsonify({"status": "ok", "classes": len(labels)})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        img_bytes = None

        if request.is_json:
            data = request.get_json()
            image_data = data.get("image", "")
            if "," in image_data:
                image_data = image_data.split(",", 1)[1]
            img_bytes = base64.b64decode(image_data)
        elif "file" in request.files:
            img_bytes = request.files["file"].read()
        else:
            return jsonify({"error": "No image data provided"}), 400

        image = Image.open(io.BytesIO(img_bytes))
        tensor = preprocess_pil(image)

        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0]
            idx = int(torch.argmax(probs))
            predicted_label = labels[idx]
            confidence = float(probs[idx]) * 100

            all_scores = {
                labels[i]: round(float(probs[i]) * 100, 2)
                for i in range(len(labels))
            }

        is_target = predicted_label in TARGETS
        status = "TARGET / ALERT" if is_target else "NEGATIVE / COMPARATOR"

        return jsonify({
            "label": predicted_label,
            "confidence": round(confidence, 1),
            "is_target": is_target,
            "status": status,
            "color": "red" if is_target else "green",
            "all_scores": all_scores
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
