from django.core.management import BaseCommand

from localization.interface import get_trivias


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        for trivia in get_trivias(categories):
            print(trivia)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
