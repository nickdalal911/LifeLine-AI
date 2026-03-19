import numpy as np
import os
import cv2

TF_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    from tensorflow.keras.applications.efficientnet import preprocess_input
    TF_AVAILABLE = True
except:
    TF_AVAILABLE = False

# Dummy preprocess if TF not available
if not TF_AVAILABLE:
    def preprocess_input(x):
        return x

model = None

# Load model only if available
if TF_AVAILABLE and os.path.exists("best_model.h5"):
    model = load_model("best_model.h5")

classes = ["First Degree", "Second Degree", "Third Degree"]


def predict_burn(image):
    if model is None:
        return "⚠️ Model not available", 0.0

    try:
        img = cv2.resize(image, (224, 224))
        img = preprocess_input(img)
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)
        confidence = float(np.max(pred) * 100)
        label = classes[np.argmax(pred)]

        return label, confidence

    except Exception as e:
        return f"Error: {str(e)}", 0.0
