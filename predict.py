import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
import cv2

model = load_model("best_model.h5")
classes = ["First Degree", "Second Degree", "Third Degree"]

def predict_burn(image):
    img = cv2.resize(image, (224, 224))
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    confidence = float(np.max(pred) * 100)
    label = classes[np.argmax(pred)]
    return label, confidence