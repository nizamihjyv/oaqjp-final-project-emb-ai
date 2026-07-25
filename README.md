# Emotion Detector Web Application

This repository contains a Flask web application for emotion detection using the IBM Watson emotion API.

## Files
- EmotionDetection/emotion_detection.py: sends the request to the Watson emotion service and returns emotion scores.
- server.py: exposes the Flask routes for the web UI.
- templates/index.html: provides the input form and result container.
- test_emotion_detection.py: exercises the detector behavior for the required sample phrases.

## Run locally
1. Install dependencies: `pip install flask requests`
2. Start the server: `python server.py`
3. Open http://127.0.0.1:5000/
