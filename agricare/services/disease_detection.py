import json
import uuid
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf

from PIL import Image
from agricare.database.db import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "best_potato_model.keras"
CLASS_PATH = PROJECT_ROOT / "models" / "class_names.json"
UPLOAD_DIR = PROJECT_ROOT / "uploads"


@st.cache_resource
def load_disease_model():
    return tf.keras.models.load_model(str(MODEL_PATH), compile=False)


def predict_disease(image):
    model = load_disease_model()

    with open(CLASS_PATH, "r") as file:
        class_names = json.load(file)["class_names"]

    image = image.convert("RGB").resize((128, 128))
    image_array = np.asarray(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array, verbose=0)[0]
    predicted_index = int(np.argmax(predictions))

    probabilities = {
        class_names[i]: float(predictions[i])
        for i in range(len(class_names))
    }

    return class_names[predicted_index], float(predictions[predicted_index]), probabilities


def save_scan(user_id, farm_id, image, predicted_class, confidence, probabilities):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    image_path = UPLOAD_DIR / filename

    image.convert("RGB").save(image_path, format="JPEG", quality=90)

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO scans (
                    user_id, farm_id, image_path,
                    predicted_class, confidence, probabilities_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    farm_id,
                    str(image_path),
                    predicted_class,
                    confidence,
                    json.dumps(probabilities)
                )
            )
        return True, "Scan saved successfully!"

    except Exception as error:
        if image_path.exists():
            image_path.unlink()
        return False, f"Could not save scan: {error}"