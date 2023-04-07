from django.test import TestCase

from trivia_client.utils import get_category_ids_by_names


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
