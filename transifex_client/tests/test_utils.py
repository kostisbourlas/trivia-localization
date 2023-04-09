from django.test import TestCase

from transifex_client.utils import slugify_string


class SlugifyStringTest(TestCase):
    def test_slugify_string_with_spaces_and_special_characters(self):
        input_string = "This! is! a string that needs to be slugified!#"
        expected_output = "this-is-a-string-that-needs-to-be-slugified"
        self.assertEqual(slugify_string(input_string), expected_output)

    def test_slugify_string_with_uppercase_letters(self):
        input_string = "This Is A Test String"
        expected_output = "this-is-a-test-string"
        self.assertEqual(slugify_string(input_string), expected_output)

    def test_slugify_string_with_already_slugified_string(self):
        input_string = "this-is-already-slugified"
        expected_output = "this-is-already-slugified"
        self.assertEqual(slugify_string(input_string), expected_output)
