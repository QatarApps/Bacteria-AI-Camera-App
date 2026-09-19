import cv2
import torch
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).with_name("bacteria_classifier_torchscript.pt")
LABELS_PATH = Path(__file__).with_name("bacteria_labels.txt")
IMAGE_SIZE = 80
TARGETS = {"Pseudomonas_aeruginosa", "Staphylococcus_aureus"}

labels = [x.strip() for x in LABELS_PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
model = torch.jit.load(str(MODEL_PATH), map_location="cpu")
model.eval()

def preprocess(frame):
    # Match training preprocessing: RGB, resize 80x80, tensor, normalize to [-1,1].
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = cv2.resize(rgb, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_AREA)
    x = torch.from_numpy(rgb).permute(2, 0, 1).float() / 255.0
    x = (x - 0.5) / 0.5
    return x.unsqueeze(0)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Camera not found. Try another camera index such as 1.")

    print("Press Q inside the camera window to quit.")
    with torch.no_grad():
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            logits = model(preprocess(frame))
            probs = torch.softmax(logits, dim=1)[0]
            idx = int(torch.argmax(probs))
            label = labels[idx]
            confidence = float(probs[idx]) * 100

            # Red for either research target; green for comparator/negative classes.
            color = (0, 0, 255) if label in TARGETS else (0, 255, 0)
            status = "TARGET / ALERT" if label in TARGETS else "NEGATIVE / COMPARATOR"
            text = f"{label} | {confidence:.1f}% | {status}"

            cv2.rectangle(frame, (8, 8), (frame.shape[1]-8, 55), color, 3)
            cv2.putText(frame, text, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
            cv2.imshow("Bacteria AI - Research Prototype", frame)

            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
