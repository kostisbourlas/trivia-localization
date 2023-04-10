import os
import json

from django.test import TestCase
from django.conf import settings

from localization.utils import append_data_to_file, remove_files


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
