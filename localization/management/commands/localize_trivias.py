from django.core.management import BaseCommand

from localization.interface import get_trivias
from localization.service import construct_trivia_format
from localization.utils import append_data_to_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        for trivia in get_trivias(categories):
            trivia_data: dict = construct_trivia_format(trivia)
            append_data_to_file(
                trivia_data, f"{trivia.get('category')}_trivia.json"
            )

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
