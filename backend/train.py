import argparse
import os
import re
from glob import glob
from typing import List, Tuple

from PIL import Image

from model import train_model, save_model


def guess_label_from_path(path: str) -> str:
    fname = os.path.basename(path)
    stem, _ = os.path.splitext(fname)
    # Prefer parent directory if it's a class folder
    parent = os.path.basename(os.path.dirname(path))
    if parent and parent.lower() not in {"", ".", "data", "train", "images", "img"}:
        return parent
    # Else parse letters until first digit/underscore
    m = re.match(r"([A-Za-z]+)", stem)
    return m.group(1) if m else stem


def collect_images(data_dir: str) -> Tuple[List[str], List[str]]:
    exts = ["*.jpg", "*.jpeg", "*.png"]
    paths: List[str] = []
    for ext in exts:
        paths.extend(glob(os.path.join(data_dir, "**", ext), recursive=True))
    paths = [p for p in paths if os.path.isfile(p)]
    labels = [guess_label_from_path(p) for p in paths]
    return paths, labels


def main():
    parser = argparse.ArgumentParser(description="Train simple color-hist SVC for disease classification")
    parser.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "..", "test"), help="Directory containing training images (classes by folder or filename prefix)")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "model", "model.joblib"), help="Output model path")
    args = parser.parse_args()

    data_dir = os.path.abspath(args.data_dir)
    out_path = os.path.abspath(args.out)
    print(f"Loading images from: {data_dir}")
    X_paths, y = collect_images(data_dir)
    if len(X_paths) < 2:
        raise SystemExit("Not enough images found to train a model. Provide at least 2 images from 2 classes.")

    print(f"Found {len(X_paths)} images across {len(set(y))} classes: {sorted(set(y))}")
    model = train_model(X_paths, y, use_svc=True)
    save_model(model, out_path)
    print(f"Saved model to: {out_path}")


if __name__ == "__main__":
    main()
