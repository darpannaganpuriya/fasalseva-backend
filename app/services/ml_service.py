import os
import logging
from typing import Any

import joblib
import numpy as np

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "ml_models")

shelf_life_model: Any = None
price_model: Any = None
le_crop: Any = None
le_state: Any = None
le_district: Any = None


def load_models_on_startup() -> None:
    global shelf_life_model, price_model, le_crop, le_state, le_district

    if shelf_life_model is not None:
        return

    model_paths = {
        "shelf_life": os.path.join(MODEL_DIR, "spoilage_classifier.pkl"),
        "price": os.path.join(MODEL_DIR, "price_model.pkl"),
        "crop": os.path.join(MODEL_DIR, "le_crop.pkl"),
        "state": os.path.join(MODEL_DIR, "le_state.pkl"),
        "district": os.path.join(MODEL_DIR, "le_district.pkl"),
    }

    for name, path in model_paths.items():
        if not os.path.exists(path):
            logger.warning("Model file not found at %s; using fallback behavior", path)

    def safe_load(path: str) -> Any:
        if os.path.exists(path):
            try:
                return joblib.load(path)
            except Exception as e:
                logger.error("Failed to load model from %s: %s", path, e)
        return None

    shelf_life_model = safe_load(model_paths["shelf_life"])
    price_model = safe_load(model_paths["price"])
    le_crop = safe_load(model_paths["crop"])
    le_state = safe_load(model_paths["state"])
    le_district = safe_load(model_paths["district"])

    logger.info("ML models loaded")


def predict_shelf_life(crop: str, temperature: float, humidity: float, days_stored: float) -> dict[str, Any]:
    if shelf_life_model is None:
        base_days = {"Tomato": 10, "Potato": 60, "Onion": 90, "Banana": 8, "Mango": 12, "Cauliflower": 9, "Cabbage": 20, "Spinach": 5, "Grapes": 14, "Guava": 10, "Carrot": 25, "Brinjal": 8, "Wheat": 180, "Rice": 180}.get(crop, 30)
        temp_penalty = max(0, (temperature - 15) * 0.15)
        humidity_penalty = max(0, (humidity - 70) * 0.02)
        raw = base_days * (1 - temp_penalty * 0.05 - humidity_penalty)
        days_remaining = max(0, int(round(raw - days_stored)))
        ratio = days_remaining / base_days if base_days else 1
        risk_level = "Green" if ratio > 0.5 else "Yellow" if ratio > 0.2 else "Red"
        return {"days_remaining": days_remaining, "risk_level": risk_level, "confidence": 0.72, "recommendation": "Use controlled storage to prevent further loss"}

    features = np.array([[0, 0, temperature, humidity, days_stored]], dtype=float)
    prediction = shelf_life_model.predict(features)[0]
    return {"days_remaining": int(abs(prediction)), "risk_level": "Green" if prediction > 6 else "Yellow" if prediction > 3 else "Red", "confidence": 0.8, "recommendation": "Use controlled storage to prevent further loss"}


def predict_price(crop: str, state: str, district: str, current_price: float, month: int, week: int) -> dict[str, Any]:
    if price_model is None:
        trend = "Stable"
        predicted_price = int(round(current_price * 1.05))
        return {"current_price": float(current_price), "predicted_price": float(predicted_price), "difference": float(predicted_price - current_price), "trend": trend, "confidence": 0.74}

    encoded_crop = le_crop.transform([crop])[0] if le_crop is not None else 0
    encoded_state = le_state.transform([state])[0] if le_state is not None else 0
    encoded_district = le_district.transform([district])[0] if le_district is not None else 0
    features = np.array([[encoded_crop, encoded_state, encoded_district, current_price, month, week]], dtype=float)
    predicted_price = float(price_model.predict(features)[0])
    difference = predicted_price - current_price
    if difference > current_price * 0.04:
        trend = "Increasing"
    elif difference < -current_price * 0.04:
        trend = "Decreasing"
    else:
        trend = "Stable"
    return {"current_price": float(current_price), "predicted_price": float(round(predicted_price)), "difference": float(round(difference)), "trend": trend, "confidence": 0.82}
