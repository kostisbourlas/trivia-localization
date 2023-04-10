import os
import json

from django.test import TestCase
from django.conf import settings

from localization.objects import Resource
from localization.utils import append_data_to_file, remove_files, \
    get_resource_from_storage, category_exists_in_resources


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
