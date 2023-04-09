from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import get_trivias, create_resource, \
    upload_file_to_resource
from localization.service import construct_trivia_format
from localization.utils import append_data_to_file, remove_files


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        filepath_resource_mapper: dict = {}
        for trivia in get_trivias(categories):
            response = create_resource(trivia.get("category"))
            resource_id = response.get("data").get("id")

            trivia_data: dict = construct_trivia_format(trivia)
            filepath, filename = append_data_to_file(
                trivia_data,
                f"{trivia.get('category')}{settings.TRIVIA_FILES_SUFFIX}.json"
            )

            filepath_resource_mapper[resource_id] = (filepath, filename)

        for resource, file_details in filepath_resource_mapper.items():
            with open(file_details[0], 'rb') as file:
                print(file)
                upload_file_to_resource(file, file_details[1], resource)
                _ = remove_files(file_details)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
