"""Flask server for the emotion detection web application."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_endpoint():
    """Analyze user input and display the emotion results."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    results = emotion_detector(text_to_analyze)
    return (
        f"<p>Anger: {results['anger']}</p>"
        f"<p>Disgust: {results['disgust']}</p>"
        f"<p>Fear: {results['fear']}</p>"
        f"<p>Joy: {results['joy']}</p>"
        f"<p>Sadness: {results['sadness']}</p>"
        f"<p>Dominant Emotion: {results['dominant_emotion']}</p>"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
