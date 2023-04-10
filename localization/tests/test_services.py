from unittest import mock
from django.test import TestCase

from localization.objects import Resource
from localization.service import get_or_create_resource


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
