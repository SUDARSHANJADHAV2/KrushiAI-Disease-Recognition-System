# AI Disease Recognition (Frontend: Netlify, Backend: Render)

This project provides a minimal, production-ready split stack:
- Frontend: static HTML/CSS/JS (deploy to Netlify)
- Backend: Python Flask API with scikit-learn model (deploy to Render)

## Structure
- frontend/ — static site (index.html, styles.css, script.js, config.js)
- backend/ — Flask app (app.py), training utilities (train.py, model.py), requirements.txt

## Local dev
1) Backend
- python -m venv .venv && source .venv/bin/activate  (Windows: .venv\\Scripts\\activate)
- pip install -r backend/requirements.txt
- (optional) Train a model using your dataset:
  python backend/train.py --data-dir <path-to-images> --out backend/model/model.joblib
- python backend/app.py

2) Frontend
- Open frontend/index.html in a browser OR serve with any static server
- Set frontend/config.js: window.API_BASE_URL = "http://localhost:5000"

## Deploy backend to Render
- Connect repository on https://render.com
- Use render.yaml in the repo (auto-detected) OR configure manually:
  - Root Directory: backend
  - Build Command: pip install -r requirements.txt
  - Start Command: gunicorn app:app --preload --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT
- Upload a trained model to backend/model/model.joblib (commit it or attach storage). If not present, API returns 503 with instructions.
- Verify health at GET /

## Deploy frontend to Netlify
- Create a new site from this repository and set Base directory: frontend (or drag-drop the frontend folder)
- No build command needed, publish directory: frontend
- In frontend/config.js, set window.API_BASE_URL to your Render backend URL

## API
- POST /predict-image — multipart/form-data with key "file"
  Response: { ok, label, scores: { class: probability } }

## Notes
- The included training script uses simple color-histogram features and SVC; replace with a stronger pipeline as needed.
- CORS is enabled for all origins on the backend for simplicity.
