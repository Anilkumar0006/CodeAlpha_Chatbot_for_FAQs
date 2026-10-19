"""
Unit Tests for College FAQ Chatbot (Student Project)
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, preprocess_text, get_chatbot_response


class TestCollegeChatbot(unittest.TestCase):
    """Test suite for preprocessing, chatbot matching, and Flask routes"""

    def setUp(self):
        self.client = app.test_client()

    def test_preprocessing(self):
        # Checks lowercase, punctuation removal, and token cleaning
        text = "What is the B.Tech Fee?!?"
        cleaned = preprocess_text(text)
        self.assertNotIn("?", cleaned)
        self.assertNotIn("!", cleaned)
        self.assertTrue(cleaned.islower())

    def test_fee_query(self):
        answer = get_chatbot_response("What is the fee for B.Tech?")
        self.assertIn("85,000", answer)

    def test_attendance_query(self):
        answer = get_chatbot_response("What is the minimum attendance percentage?")
        self.assertIn("75%", answer)

    def test_placement_query(self):
        answer = get_chatbot_response("Which companies visit for campus placements?")
        self.assertIn("TCS", answer)

    def test_greeting_query(self):
        answer = get_chatbot_response("hello")
        self.assertIn("Hello", answer)

    def test_fallback_query(self):
        answer = get_chatbot_response("How to cook pasta?")
        self.assertEqual(answer, "Sorry, I could not find a suitable answer. Please try another question.")

    def test_empty_query(self):
        answer = get_chatbot_response("")
        self.assertEqual(answer, "Please type a question so I can assist you.")

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"College FAQ Chatbot", response.data)

    def test_get_response_api(self):
        payload = {"message": "When are the semester exams conducted?"}
        response = self.client.post(
            "/get_response",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("answer", data)
        self.assertIn("December", data["answer"])


if __name__ == "__main__":
    unittest.main()
