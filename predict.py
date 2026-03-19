import numpy as np
import os

try:
    import cv2
except:
    cv2 = None

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
MODEL_PATH = "best_model.h5"

# ✅ DOWNLOAD MODEL FROM GOOGLE DRIVE IF NOT PRESENT
if TF_AVAILABLE:
    if not os.path.exists(MODEL_PATH):
        try:
            import gdown
            url = "https://drive.google.com/uc?id=1qLfQ4896g74yrp5ziLM3y6QJQ5sFGSSK"
            gdown.download(url, MODEL_PATH, quiet=False)
        except Exception as e:
            print("Model download failed:", e)

    # ✅ LOAD MODEL AFTER DOWNLOAD
    if os.path.exists(MODEL_PATH):
        try:
            model = load_model(MODEL_PATH)
            print("Model loaded successfully")
        except Exception as e:
            print("Model loading failed:", e)

classes = ["First Degree", "Second Degree", "Third Degree"]


def predict_burn(image):
    try:
        # ✅ IF MODEL AVAILABLE → USE REAL PREDICTION
        if model is not None:
            img = cv2.resize(image, (224, 224))
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)

            preds = model.predict(img)
            class_idx = np.argmax(preds)
            confidence = float(np.max(preds) * 100)

            return classes[class_idx], confidence

        # ✅ FALLBACK (your original logic)
        avg_pixel = image.mean()

        if avg_pixel > 180:
            return "First Degree", 65.0
        elif avg_pixel > 100:
            return "Second Degree", 82.5
        else:
            return "Third Degree", 91.2

    except Exception as e:
        return f"Error: {str(e)}", 0.0
