import io
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import joblib
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler


def _ensure_rgb(img: Image.Image) -> Image.Image:
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def extract_features(img: Image.Image, bins: int = 8, size: Tuple[int, int] = (128, 128)) -> np.ndarray:
    """
    Compute a simple color histogram feature vector.
    - Resize to size
    - 8-bin histogram per RGB channel
    Returns shape (bins*3,)
    """
    img = _ensure_rgb(img).resize(size)
    arr = np.asarray(img)
    feats: List[np.ndarray] = []
    for c in range(3):
        hist, _ = np.histogram(arr[:, :, c], bins=bins, range=(0, 256), density=True)
        feats.append(hist.astype(np.float32))
    vec = np.concatenate(feats, axis=0)
    # L2 normalize for stability
    norm = np.linalg.norm(vec) + 1e-8
    return (vec / norm).astype(np.float32)


@dataclass
class TrainedModel:
    pipeline: Pipeline
    label_encoder: LabelEncoder

    def predict(self, img: Image.Image) -> Tuple[str, Dict[str, float]]:
        x = extract_features(img).reshape(1, -1)
        if hasattr(self.pipeline, "predict_proba"):
            proba = self.pipeline.predict_proba(x)[0]
        else:
            # Fallback: use decision function, convert to pseudo-probabilities
            scores = self.pipeline.decision_function(x)
            # Softmax-like conversion
            exps = np.exp(scores - np.max(scores))
            proba = exps / np.sum(exps)
        idx = int(np.argmax(proba))
        label = str(self.label_encoder.inverse_transform([idx])[0])
        probs = {cls: float(p) for cls, p in zip(self.label_encoder.classes_, proba)}
        # Sort probabilities by descending
        probs = dict(sorted(probs.items(), key=lambda kv: kv[1], reverse=True))
        return label, probs


def train_model(image_paths: List[str], labels: List[str], use_svc: bool = True) -> TrainedModel:
    X = []
    for p in image_paths:
        with Image.open(p) as im:
            X.append(extract_features(im))
    X = np.vstack(X)

    le = LabelEncoder()
    y = le.fit_transform(labels)

    if use_svc:
        clf = SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight="balanced", random_state=42)
    else:
        clf = LogisticRegression(max_iter=2000, class_weight="balanced", n_jobs=None)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", clf),
    ])
    pipe.fit(X, y)

    return TrainedModel(pipeline=pipe, label_encoder=le)


def save_model(model: TrainedModel, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump({
        "pipeline": model.pipeline,
        "label_encoder": model.label_encoder,
    }, path)


def load_model(path: str) -> TrainedModel | None:
    if not os.path.exists(path):
        return None
    data = joblib.load(path)
    return TrainedModel(pipeline=data["pipeline"], label_encoder=data["label_encoder"]) 
