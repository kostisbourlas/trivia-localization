from django.core.management import BaseCommand

from localization.service import (
    upload_files_to_resources,
    prepare_trivias_to_upload
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        resource_file_storage = prepare_trivias_to_upload(categories)

        upload_files_to_resources(resource_file_storage)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
