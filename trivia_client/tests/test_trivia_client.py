from unittest.mock import patch, MagicMock

from django.test import TestCase

from trivia_client.exceptions import EmptyCategoryListError
from trivia_client.trivia_client import TriviaClient


class TriviaClientTestCase(TestCase):
    def setUp(self):
        self.mock_response = {
            "response_code": 0,
            "results": [
                {
                    "category": "General Knowledge",
                    "type": "multiple",
                    "difficulty": "easy",
                    "question": "What is the capital of Australia?",
                    "correct_answer": "Canberra",
                    "incorrect_answers": ["Sydney", "Melbourne", "Perth"]
                },
            ]
        }
        self.mock_categories = {
            "trivia_categories": [
                {"id": 1, "name": "General Knowledge"},
                {"id": 2, "name": "Geography"}
            ]
        }
        self.client = TriviaClient(cache=None)

    @patch("trivia_client.utils.call_url_async")
    def test_get_trivias_by_categories(self, call_url_mock):
        call_url_mock.return_value = self.mock_response

        categories = {"General Knowledge"}
        expected_trivias = self.mock_response.get("results")

        with patch.object(
            TriviaClient, '_get_categories', return_value=self.mock_categories
        ):
            trivias = self.client.get_trivias_by_categories(categories)

        self.assertEqual(trivias, expected_trivias)

    def test_get_trivias_by_categories_with_empty_categories(self):
        categories = set()

        with self.assertRaises(EmptyCategoryListError):
            self.client.get_trivias_by_categories(categories)
