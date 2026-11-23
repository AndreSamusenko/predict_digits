"""Regenerate weights.js from the project's Keras model (requires h5py)."""
import base64
from pathlib import Path
import h5py

web = Path(__file__).resolve().parent
with h5py.File(web.parent / "src/mlp_digits_28x28.h5") as model:
    arrays = [
        model[f"model_weights/{layer}/{layer}/{param}:0"][()].astype("<f4")
        for layer in ("conv2d_2", "conv2d_3", "dense_1")
        for param in ("kernel", "bias")
    ]
encoded = base64.b64encode(b"".join(a.tobytes() for a in arrays)).decode()
(web / "weights.js").write_text(f'const encodedWeights = "{encoded}";\n')
