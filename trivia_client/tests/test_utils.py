from django.test import TestCase

from trivia_client.utils import (
    get_category_ids_by_names,
    get_results_from_responses
)


class GetCategoryIdsByNames(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category_list = [
            {"id": 1, "name": "General Knowledge"},
            {"id": 2, "name": "Mythology"},
            {"id": 3, "name": "Sports"},
        ]

    def test_get_category_ids_given_a_set_of_names(self):
        names = {"Sports", "Mythology"}
        correct_ids = {3, 2}

        category_ids = get_category_ids_by_names(self.category_list, names)

        self.assertSetEqual(correct_ids, category_ids)


class GetResultsFromResponsesTestCase(TestCase):
    def test_returns_empty_list_when_given_empty_list(self):
        responses = []
        results = get_results_from_responses(responses)
        self.assertEqual(results, [])

    def test_returns_the_list_of_results(self):
        responses = [
            {"count": 2, "results": [{"name": "Resource 1"}, {"name": "Resource 2"}]},
            {"count": 1, "results": [{"name": "Resource 3"}]},
        ]
        results = get_results_from_responses(responses)
        expected_results = [
            {"name": "Resource 1"}, {"name": "Resource 2"}, {"name": "Resource 3"}
        ]
        self.assertEqual(results, expected_results)

    def test_returns_empty_list_when_no_results_found(self):
        responses = [
            {"count": 0, "results": []},
            {"count": 0, "results": []},
        ]
        results = get_results_from_responses(responses)
        self.assertEqual(results, [])