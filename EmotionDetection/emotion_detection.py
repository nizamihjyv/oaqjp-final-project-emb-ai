"""Emotion detection helpers for the Flask web application."""

import requests

API_URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyse):
    """Send text to the Watson emotion API and return the parsed scores."""
    if not text_to_analyse or not text_to_analyse.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    payload = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    response_payload = response.json()
    emotion_scores = response_payload.get("emotion", {})
    scores = {}
    for emotion in EMOTION_KEYS:
        score = emotion_scores.get(emotion, {}).get("score")
        scores[emotion] = score

    valid_scores = {key: value for key, value in scores.items() if value is not None}
    dominant_emotion = None
    if valid_scores:
        dominant_emotion = max(valid_scores, key=valid_scores.get)

    return {
        **scores,
        "dominant_emotion": dominant_emotion,
    }
