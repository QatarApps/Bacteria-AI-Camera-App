# Bacteria AI Classifier & Camera App 🔬

A real-time AI computer vision application for classifying bacterial species under microscope or camera feeds using PyTorch TorchScript.

## 🎯 Target Pathogens vs Comparator Classes

The model classifies 5 microscopic classes into two operational categories:

| Category | Color Alert | Species |
| :--- | :---: | :--- |
| **TARGET / ALERT** | 🔴 **RED** | *Pseudomonas aeruginosa*, *Staphylococcus aureus* |
| **NEGATIVE / COMPARATOR** | 🟢 **GREEN** | *Lactobacillus delbrueckii*, *Micrococcus spp*, *Candida albicans* |

---

## 🚀 How to Run

### Option 1: Native Windows (Direct Desktop GUI)
1. Run [`RUN_WINDOWS.bat`](RUN_WINDOWS.bat) (or run with Python):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\pip install -r requirements.txt
   .\.venv\Scripts\python camera_app.py
   ```
2. The live camera window will open. Press **Q** to quit.

---

### Option 2: Web Interface (No Docker)
1. Double-click [`RUN_WEB_LOCAL.bat`](RUN_WEB_LOCAL.bat).
2. Open your browser at `http://localhost:5000`.
3. Select your camera/microscope and click **▶ Start Camera**, or upload still photos.

---

### Option 3: Docker (Isolated Container)
1. Start **Docker Desktop**.
2. Run [`RUN_DOCKER.bat`](RUN_DOCKER.bat) or:
   ```bash
   docker compose up --build
   ```
3. Open `http://localhost:5000` in your browser.

---

## 📁 Repository Structure

```
├── bacteria_classifier_torchscript.pt  # Trained PyTorch TorchScript CNN model
├── bacteria_labels.txt                # Class names recognized by the model
├── camera_app.py                      # Real-time OpenCV desktop camera script
├── web_app.py                         # Flask web inference backend
├── templates/
│   └── index.html                     # Web camera UI with live bounding alerts
├── Dockerfile                         # CPU-optimized Docker container image
├── docker-compose.yml                 # Docker Compose service definition
├── requirements.txt                   # Desktop Python dependencies
├── requirements_docker.txt            # Docker minimal web dependencies
├── RUN_WINDOWS.bat                    # 1-click Windows desktop launcher
├── RUN_WEB_LOCAL.bat                  # 1-click local web launcher
├── RUN_DOCKER.bat                     # 1-click Docker launcher
└── README_AR.txt                      # Original Arabic instructions & disclaimer
```

---

## ⚠️ Disclaimer
This is an experimental research prototype for image classification and is **not an approved clinical diagnostic medical device**. Classification accuracy may vary significantly depending on optical quality, staining technique, microscope magnification, and lighting.
