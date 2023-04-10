from unittest import mock

from django.test import TestCase

from transifex_client.utils import slugify_string, call_url_get


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


class TestCallUrlGet(TestCase):
    @mock.patch("requests.get")
    def test_call_url_get(self, mock_requests_get):
        # Mock the response of the get method
        mock_response = mock.Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        url = "https://superduperurl.com/api"
        headers = {"User-Agent": "Test User Agent"}

        response = call_url_get(url, headers)

        mock_requests_get.assert_called_once_with(url, headers=headers)

        self.assertDictEqual(response, {"key": "value"})
