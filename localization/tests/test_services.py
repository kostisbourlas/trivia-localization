import os
from unittest import mock

import requests
from django.test import TestCase

from localization.objects import Resource, ResourceFileRelation
from localization.service import (
    _get_or_create_resource,
    _get_created_resources,
    _process_file_to_upload,
    prepare_trivias_to_upload,
)


class PrepareTriviasToUploadTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = {"Animals", "Science: Gadgets"}
        cls.trivia_response = [
            {
                'category': 'Animals',
                'question': 'The Axolotl is an amphibian that can spend its '
                            'whole life in a larval state.',
                'correct_answer': 'True',
                'incorrect_answers': 'False'
            },
            {
                'category': 'Science: Gadgets',
                'question': 'The communication protocol NFC stands for '
                            'Near-Field Control.',
                'correct_answer': 'False',
                'incorrect_answers': 'True'
             },
        ]

    @mock.patch("localization.service._get_or_create_resource")
    @mock.patch("localization.service.TriviaAPI.get_trivias")
    def test_prepare_trivias_to_upload(
        self, mock_get_trivias, mock__get_or_create_resource
    ):
        mock_get_trivias.return_value = self.trivia_response
        mock_animals_resource = Resource(
            resource_id=1, name="Animals", slug="animals"
        )
        mock_sports_resource = Resource(
            resource_id=2, name="Science: Gadgets", slug="science-gadgets"
        )
        mock__get_or_create_resource.side_effect = [
            mock_animals_resource, mock_sports_resource
        ]

        # Call the method being tested
        result = prepare_trivias_to_upload(self.categories)

        # Assert that the method returned the expected output
        expected_result = {
            ResourceFileRelation(
                resource_id=1,
                filepath="uploading_files/Animals_trivia.json",
                filename="Animals_trivia.json"
            ),
            ResourceFileRelation(
                resource_id=2,
                filepath="uploading_files/Science: Gadgets_trivia.json",
                filename="Science: Gadgets_trivia.json"
            ),
        }

        self.assertEqual(result, expected_result)

        mock_get_trivias.assert_called_once_with(self.categories)

        for relation in expected_result:
            self.assertIn(relation, result)
            os.remove(relation.filepath)

    @mock.patch("localization.service._get_or_create_resource")
    @mock.patch("localization.service.TriviaAPI.get_trivias")
    def test_prepare_trivias_to_upload_with_http_error(
        self, mock_get_trivias, mock__get_or_create_resource
    ):
        mock_get_trivias.return_value = self.trivia_response
        mock__get_or_create_resource.side_effect = requests.HTTPError()

        result: set = prepare_trivias_to_upload(self.categories)

        mock_get_trivias.assert_called_once_with(self.categories)
        mock__get_or_create_resource.assert_has_calls(
            [
                mock.call("Animals", _get_created_resources()),
                mock.call("Science: Gadgets", _get_created_resources())
            ]
        )
        self.assertEqual(len(result), 0)


class ProcessFileToUploadTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = ResourceFileRelation(
            resource_id=1,
            filename='test.json',
            filepath='uploading_files/test.json',
        )

    @mock.patch('localization.service.call_url_with_retry')
    @mock.patch('localization.service.call_url_with_polling')
    @mock.patch('localization.service.TransifexAPI.get_resource_data')
    def test_process_file_to_upload_success(
        self, get_resource_data, mock_polling, mock_retry
    ):
        existing_data = {'foo': 'bar'}
        get_resource_data.return_value = existing_data
        mock_retry.return_value = {'data': {'id': '123'}}
        mock_polling.return_value = {
            'data': {'attributes': {'status': 'succeeded'}}
        }

        failed_upload = _process_file_to_upload(self.item)

        # Assert that the file was uploaded successfully and the method
        # returns None
        self.assertIsNone(failed_upload)

        get_resource_data.assert_called_once_with(
            self.item.resource_id
        )

    @mock.patch('localization.service.call_url_with_retry')
    @mock.patch('localization.service.call_url_with_polling')
    @mock.patch('localization.service.TransifexAPI.get_resource_data')
    def test_process_file_to_upload_with_http_error(
        self, get_resource_data, mock_polling, mock_retry
    ):
        existing_data = {'foo': 'bar'}
        get_resource_data.return_value = existing_data
        mock_retry.side_effect = requests.HTTPError()
        mock_polling.return_value = {
            'data': {'attributes': {'status': 'succeeded'}}
        }

        failed_upload = _process_file_to_upload(self.item)

        self.assertEqual(failed_upload, self.item)

    @mock.patch('localization.service.call_url_with_retry')
    @mock.patch('localization.service.call_url_with_polling')
    @mock.patch('localization.service.TransifexAPI.get_resource_data')
    def test_process_file_to_upload_fails_in_polling(
        self, get_resource_data, mock_polling, mock_retry
    ):
        existing_data = {'foo': 'bar'}
        get_resource_data.return_value = existing_data
        mock_retry.side_effect = requests.HTTPError()
        mock_polling.return_value = {
            'data': {'attributes': {'status': 'failed'}}
        }

        failed_upload = _process_file_to_upload(self.item)

        self.assertEqual(failed_upload, self.item)



class GetOrCreateResourceTestCase(TestCase):
    def setUp(self):
        self.resource1 = Resource(
            resource_id=1, name="Resource 1", slug="resource-1"
        )
        self.resources = {self.resource1}

    @mock.patch('localization.service.TransifexAPI.create_resource')
    def test_get_or_create_resource_resource_exists(self, mock_create_resource):
        # Call the method being tested with an existing category name
        result = _get_or_create_resource(self.resource1.name, self.resources)

        # Assert that the method returned the expected Resource object
        self.assertEqual(result, self.resource1)

        # Assert that TransifexAPI.create_resource() was not called
        mock_create_resource.assert_not_called()

    @mock.patch('localization.service.TransifexAPI.create_resource')
    def test_get_or_create_resource_resource_does_not_exist(
        self, mock_create_resource
    ):
        resource_id = 2
        resource_name = "Resource 2"
        resource_slug = "resource-2"
        mock_create_resource.return_value = {
            "data": {
                "id": resource_id,
                "attributes": {
                    "name": resource_name,
                    "slug": resource_slug
                }
            }
        }

        # Call the method being tested with a nonexistent category name
        result = _get_or_create_resource("Resource 2", self.resources)

        # Assert that the method returned the expected Resource object
        self.assertEqual(result.resource_id, resource_id)
        self.assertEqual(result.name, resource_name)
        self.assertEqual(result.slug, resource_slug)

        # Assert that TransifexAPI.create_resource() was called with the correct
        # parameters
        mock_create_resource.assert_called_once_with(resource_name)


class GetCreatedResourcesTestCase(TestCase):
    @mock.patch('localization.service.TransifexAPI.get_all_resources')
    def test_get_created_resources(self, mock_get_all_resources):
        # Create mock data for the TransifexAPI.get_all_resources response
        mock_data = {
            "data": [
                {
                    "id": "123",
                    "attributes": {
                        "name": "Resource 1",
                        "slug": "resource-1"
                    }
                },
                {
                    "id": "456",
                    "attributes": {
                        "name": "Resource 2",
                        "slug": "resource-2"
                    }
                }
            ]
        }
        mock_get_all_resources.return_value = mock_data

        # Call the get_created_resources method and check the result
        created_resources = _get_created_resources()
        self.assertEqual(len(created_resources), 2)

    @mock.patch('localization.service.TransifexAPI.get_all_resources')
    def test_get_created_resources_with_no_results(
        self, mock_get_all_resources
    ):
        # Create mock data for the TransifexAPI.get_all_resources response
        mock_data = {}
        mock_get_all_resources.return_value = mock_data

        created_resources = _get_created_resources()
        self.assertFalse(bool(created_resources))
