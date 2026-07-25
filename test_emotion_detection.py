"""Tests for the emotion detector module."""

import unittest
from unittest.mock import patch

from EmotionDetection.emotion_detection import emotion_detector


class FakeResponse:
    """Simple response stub for mocked HTTP calls."""

    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        """Return the payload from the fake response."""
        return self._payload


class EmotionDetectorTests(unittest.TestCase):
    """Verify dominant emotion selection and 400 handling."""

    def test_emotion_detector_matches_expected_dominant_emotions(self):
        """Each sample sentence should map to the expected dominant emotion."""
        cases = [
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        ]

        for text, expected_emotion in cases:
            payload = {
                "emotionPredictions": [
                    {
                        "emotion": {
                            "anger": 0.1,
                            "disgust": 0.1,
                            "fear": 0.1,
                            "joy": 0.1,
                            "sadness": 0.1,
                        }
                    }
                ]
            }
            if expected_emotion == "joy":
                payload["emotionPredictions"][0]["emotion"]["joy"] = 0.9
            elif expected_emotion == "anger":
                payload["emotionPredictions"][0]["emotion"]["anger"] = 0.9
            elif expected_emotion == "disgust":
                payload["emotionPredictions"][0]["emotion"]["disgust"] = 0.9
            elif expected_emotion == "sadness":
                payload["emotionPredictions"][0]["emotion"]["sadness"] = 0.9
            elif expected_emotion == "fear":
                payload["emotionPredictions"][0]["emotion"]["fear"] = 0.9

            with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
                mock_post.return_value = FakeResponse(200, payload)
                result = emotion_detector(text)

            self.assertEqual(result["dominant_emotion"], expected_emotion)

    def test_emotion_detector_returns_none_fields_for_bad_request(self):
        """A 400 response should return None values for all emotion fields."""
        with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
            mock_post.return_value = FakeResponse(400, {})
            result = emotion_detector("bad input")

        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
