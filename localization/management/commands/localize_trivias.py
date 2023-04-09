from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import get_trivias, create_resource, \
    get_all_resources
from localization.service import construct_trivia_format, \
    upload_files_to_resources
from localization.utils import append_data_to_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        response = get_all_resources()
        print(response)

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

        upload_files_to_resources(filepath_resource_mapper)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
