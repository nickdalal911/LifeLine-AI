import numpy as np
import os

try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except:
    TF_AVAILABLE = False
from tensorflow.keras.applications.efficientnet import preprocess_input
import cv2

model = None

if TF_AVAILABLE and os.path.exists("best_model.h5"):
    model = load_model("best_model.h5")



model = load_model("best_model.h5")
classes = ["First Degree", "Second Degree", "Third Degree"]

def predict_burn(image):
    # If model not available
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
