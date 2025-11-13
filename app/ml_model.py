"""
ML Model utilities for EVBot.

Centralises model loading, preprocessing, and prediction helpers so the
Flask views and chatbot can share the same logic.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, List, Tuple

import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "ev_model.pkl")
ENCODERS_PATH = os.path.join(BASE_DIR, "models", "label_encoders.pkl")

# (incoming_key, dataframe_column_name, caster)
FEATURE_SPECS: List[Tuple[str, str, Any]] = [
    ("soc", "SOC (%)", float),
    ("voltage", "Voltage (V)", float),
    ("current", "Current (A)", float),
    ("battery_temp", "Battery Temp (°C)", float),
    ("ambient_temp", "Ambient Temp (°C)", float),
    ("duration", "Charging Duration (min)", float),
    ("degradation", "Degradation Rate (%)", float),
    ("mode", "Charging Mode", str),
    ("efficiency", "Efficiency (%)", float),
    ("battery_type", "Battery Type", str),
    ("cycles", "Charging Cycles", int),
    ("ev_model", "EV Model", str),
]

CLASS_MESSAGES = {
    0: "Optimal Charging: Short Duration - Excellent battery health!",
    1: "Optimal Charging: Medium Duration - Normal battery condition.",
    2: "Optimal Charging: Long Duration - Battery maintenance recommended.",
}

RESULT_TYPES = {0: "short", 1: "medium", 2: "long"}


@lru_cache(maxsize=1)
def _load_model():
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def _load_encoders():
    return joblib.load(ENCODERS_PATH)


def get_assets():
    return _load_model(), _load_encoders()


def _normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    missing: List[str] = []
    invalid: List[str] = []

    for form_key, column_name, caster in FEATURE_SPECS:
        raw_value = payload.get(form_key)
        if raw_value in (None, ""):
            missing.append(form_key)
            continue

        try:
            if caster is str:
                normalized[column_name] = str(raw_value).strip()
            else:
                normalized[column_name] = caster(raw_value)
        except (TypeError, ValueError):
            invalid.append(form_key)

    if missing:
        raise ValueError(
            f"Missing required fields for prediction: {', '.join(missing)}"
        )

    if invalid:
        raise ValueError(
            f"Invalid values provided for: {', '.join(invalid)}"
        )

    return normalized


def build_feature_frame(payload: Dict[str, Any]) -> pd.DataFrame:
    normalized = _normalize_payload(payload)
    return pd.DataFrame(
        {column: [normalized[column]] for _, column, _ in FEATURE_SPECS}
    )


def encode_categorical_features(features: pd.DataFrame) -> pd.DataFrame:
    _, encoders = get_assets()
    encoded = features.copy()

    for _, column_name, caster in FEATURE_SPECS:
        if caster is str:
            encoder = encoders.get(column_name)
            if encoder is None:
                raise ValueError(
                    f"Encoder not found for column '{column_name}'."
                )
            encoded[column_name] = encoder.transform(encoded[column_name])

    return encoded


def predict_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    features = build_feature_frame(payload)
    encoded_features = encode_categorical_features(features)
    model, _ = get_assets()

    prediction = int(model.predict(encoded_features)[0])
    message = CLASS_MESSAGES.get(
        prediction, f"Prediction: Class {prediction}"
    )
    result_type = RESULT_TYPES.get(prediction, "short")

    return {
        "class_id": prediction,
        "result_type": result_type,
        "message": message,
        "inputs": features.iloc[0].to_dict(),
    }
