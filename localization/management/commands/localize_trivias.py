from typing import Set

from django.core.management import BaseCommand

from localization.objects import ResourceFileRelation
from localization.service import (
    process_files_to_upload,
    prepare_trivias_to_upload
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        resource_file_storage = prepare_trivias_to_upload(categories)

        failed_uploads: Set[ResourceFileRelation] = process_files_to_upload(
            resource_file_storage
        )
        if failed_uploads:
            self.stdout.write(
                self.style.ERROR(
                    "The following files couldn't be uploaded:", failed_uploads
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("Command successfully ran"))
