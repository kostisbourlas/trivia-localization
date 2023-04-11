import os
import json
from unittest import mock

import requests

from unittest.mock import Mock, MagicMock

from django.test import TestCase
from django.conf import settings

from localization.exceptions import NonPositiveNumberError
from localization.objects import Resource
from localization.utils import (
    append_data_to_file,
    remove_files,
    get_resource_from_storage,
    category_exists_in_resources,
    get_dict_path,
    call_url_with_polling,
    call_url_with_retry,
    decode_string,
    decode_dict_values
)


class AppendDataToFileTest(TestCase):
    def setUp(self):
        self.filename = "test_file.json"
        self.file_path = f"{settings.UPLOADING_FILES_PATH}/{self.filename}"
        self.non_existing_file_path = "nonexistent_folder/nonexistent_file.json"

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_append_data_to_file(self):
        existing_data = {"a": 1, "b": 2}
        new_data = {"c": 3, "d": 4}

        with open(self.file_path, "w") as file:
            json.dump(existing_data, file)

        append_data_to_file(new_data, self.filename)

        with open(self.file_path, "r") as file:
            file_data = json.load(file)

        expected_data = {"a": 1, "b": 2, "c": 3, "d": 4}
        self.assertDictEqual(file_data, expected_data)

    def test_append_data_to_new_file(self):
        data = {"a": 1, "b": 2}
        append_data_to_file(data, self.filename)

        with open(self.file_path, "r") as file:
            file_data = json.load(file)

        self.assertDictEqual(file_data, data)

    def test_append_data_to_nonexistent_path(self):
        with self.assertRaises(FileNotFoundError):
            append_data_to_file({"a": 1}, self.non_existing_file_path)


class RemoveFilesTestCase(TestCase):
    def test_remove_files_existing(self):
        filepath = "testfile.txt"
        with open(filepath, "w") as f:
            f.write("test file")

        # Call the method being tested with an existing file
        result = remove_files(filepath)

        self.assertTrue(result)
        self.assertFalse(os.path.exists(filepath))

    def test_remove_files_nonexistent(self):
        # Call the method being tested with a nonexistent file
        nonexistent_filepath = "nonexistent.txt"
        result = remove_files(nonexistent_filepath)

        self.assertFalse(result)


class GetResourceFromStorageTestCase(TestCase):
    def setUp(self):
        # Create some sample Resource objects for testing
        self.resource1 = Resource(resource_id=1, name="R 1", slug="resource-1")
        self.resource2 = Resource(resource_id=2, name="R 2", slug="resource-2")
        self.resource3 = Resource(resource_id=3, name="R 3", slug="resource-3")
        self.storage = {self.resource1, self.resource2, self.resource3}

    def test_get_resource_from_storage_found(self):
        # Call the method being tested with a valid category name
        result = get_resource_from_storage("R 2", self.storage)

        self.assertEqual(result, self.resource2)

    def test_get_resource_from_storage_not_found(self):
        # Call the method being tested with a nonexistent category name
        result = get_resource_from_storage("Resource 4", self.storage)

        self.assertIsNone(result)


class CategoryExistsInResourcesTestCase(TestCase):
    def setUp(self):
        # Create some sample Resource objects for testing
        self.resource1 = Resource(resource_id=1, name="R 1", slug="resource-1")
        self.resource2 = Resource(resource_id=2, name="R 2", slug="resource-2")
        self.resource3 = Resource(resource_id=3, name="R 3", slug="resource-3")
        self.resources = {self.resource1, self.resource2, self.resource3}

    def test_category_exists_in_resources_found(self):
        # Call the method being tested with a valid category name
        result = category_exists_in_resources("R 2", self.resources)

        self.assertTrue(result)

    def test_category_exists_in_resources_not_found(self):
        # Call the method being tested with a nonexistent category name
        result = category_exists_in_resources("Resource 4", self.resources)

        self.assertFalse(result)


class GetDictionaryPathTestCase(TestCase):
    def setUp(self):
        self.dictionary = {
            "key1": {
                "key2": {
                    "key3": "value"
                }
            }
        }

    def test_get_dict_path(self):
        result = get_dict_path(self.dictionary, "key1/key2/key3")
        self.assertEqual(result, "value")

    def test_invalid_dict_path(self):
        with self.assertRaises(KeyError):
            get_dict_path(self.dictionary, "key1/key4")


class CallUrlWithPollingTestCase(TestCase):

    def setUp(self):
        self.call_url_mock = Mock()

    @mock.patch("localization.utils.time.sleep")
    def test_call_url_with_polling_success(self, mock_time_sleep):
        mock_time_sleep.return_value = None
        self.call_url_mock.side_effect = [
            {"status": "processing"},
            {"status": "processing"},
            {"status": "done", "data": {"result": "success"}},
        ]

        retries = 3
        dict_path = "status"
        message = "done"
        expected_result = {"status": "done", "data": {"result": "success"}}

        result = call_url_with_polling(
            self.call_url_mock, retries, dict_path, message
        )

        self.assertEqual(self.call_url_mock.call_count, 3)

        self.assertEqual(result, expected_result)

    @mock.patch("localization.utils.time.sleep")
    def test_call_url_with_polling_failure(self, mock_time_sleep):
        mock_time_sleep.return_value = None
        self.call_url_mock.side_effect = [
            {"status": "processing"},
            {"status": "processing"},
            {"status": "processing"},
        ]

        retries = 3
        dict_path = "status"
        message = "done"
        expected_result = {}

        result = call_url_with_polling(
            self.call_url_mock, retries, dict_path, message
        )

        self.assertEqual(self.call_url_mock.call_count, 3)

        self.assertEqual(result, expected_result)


class TestRetryAPICall(TestCase):
    @mock.patch("localization.utils.time.sleep")
    def test_successful_call(self, mock_time_sleep):
        mock_time_sleep.return_value = None
        response_mock = {"status": "success"}

        def api_call_mock():
            return response_mock

        result = call_url_with_retry(api_call_mock, 1, set())
        self.assertEqual(result, response_mock)

    @mock.patch("localization.utils.time.sleep")
    def test_retry_on_error_code(self, mock_time_sleep):
        mock_time_sleep.return_value = None
        error_response_mock = MagicMock()
        error_response_mock.status_code = 409

        def api_call_mock():
            raise requests.HTTPError(response=error_response_mock)

        with self.assertRaises(requests.HTTPError):
            call_url_with_retry(api_call_mock, 1, {409})

    @mock.patch("localization.utils.time.sleep")
    def test_no_retry_on_unhandled_error_code(self, mock_time_sleep):
        mock_time_sleep.return_value = None
        error_response_mock = MagicMock()
        error_response_mock.status_code = 404

        def api_call_mock():
            raise requests.HTTPError(response=error_response_mock)

        with self.assertRaises(requests.HTTPError):
            call_url_with_retry(api_call_mock, 1, {500})

    def test_with_zero_retries(self):
        response_mock = {"status": "success"}

        def api_call_mock():
            return response_mock

        with self.assertRaises(NonPositiveNumberError):
            call_url_with_retry(api_call_mock, 0, {500})


class DecodeStringTestCase(TestCase):
    def test_decode_string(self):
        encoded_string = "This is a &quot;quoted&quot; string"
        decoded_string = decode_string(encoded_string)
        self.assertEqual(decoded_string, 'This is a "quoted" string')


class DecodeDictionaryTestCase(TestCase):
    def test_decode_dict_values(self):
        input_dict = {
            'key1': 'This is a &quot;quoted&quot; string',
            'key2': 'This is an &apos;apostrophized&apos; string',
            'key3': 1234
        }
        expected_dict = {
            'key1': 'This is a "quoted" string',
            'key2': "This is an 'apostrophized' string",
            'key3': 1234
        }
        decoded_dict = decode_dict_values(input_dict)
        self.assertDictEqual(decoded_dict, expected_dict)
