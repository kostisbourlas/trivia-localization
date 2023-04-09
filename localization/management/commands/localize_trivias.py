from typing import Set

from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import get_trivias, create_resource
from localization.service import construct_trivia_format
from localization.utils import append_data_to_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        filepaths: Set[str] = set()
        for trivia in get_trivias(categories):
            _ = create_resource(trivia.get("category"))

            trivia_data: dict = construct_trivia_format(trivia)
            file_path: str = append_data_to_file(
                trivia_data,
                f"{trivia.get('category')}{settings.TRIVIA_FILES_SUFFIX}.json"
            )
            filepaths.add(file_path)

        for file_path in filepaths:
            with open(file_path, 'rb') as file:
                print(file)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
