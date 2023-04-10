from unittest import mock
from django.test import TestCase

from localization.objects import Resource
from localization.service import get_or_create_resource, get_created_resources


class GetOrCreateResourceTestCase(TestCase):
    def setUp(self):
        self.resource1 = Resource(
            resource_id=1, name="Resource 1", slug="resource-1"
        )
        self.resources = {self.resource1}

    @mock.patch('localization.service.TransifexAPI.create_resource')
    def test_get_or_create_resource_resource_exists(self, mock_create_resource):
        # Call the method being tested with an existing category name
        result = get_or_create_resource(self.resource1.name, self.resources)

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
        result = get_or_create_resource("Resource 2", self.resources)

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
        created_resources = get_created_resources()
        self.assertEqual(len(created_resources), 2)

    @mock.patch('localization.service.TransifexAPI.get_all_resources')
    def test_get_created_resources_with_no_results(
        self, mock_get_all_resources
    ):
        # Create mock data for the TransifexAPI.get_all_resources response
        mock_data = {}
        mock_get_all_resources.return_value = mock_data

        created_resources = get_created_resources()
        self.assertFalse(bool(created_resources))
