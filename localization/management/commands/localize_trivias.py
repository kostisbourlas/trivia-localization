from typing import List

from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import get_trivias, create_resource
from localization.objects import ResourceFileRelation
from localization.service import (
    construct_trivia_format,
    upload_files_to_resources,
    get_created_resources
)
from localization.utils import append_data_to_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        created_resources: dict[str, tuple] = get_created_resources()

        resource_file_storage: List[ResourceFileRelation] = []
        for trivia in get_trivias(categories):
            category = trivia.get("category")
            if category not in created_resources:
                response = create_resource(category)
                resource_id = response.get("data").get("id")
                slug = response.get("data").get("attributes").get("slug")
                created_resources[category] = (resource_id, slug)

            trivia_data: dict = construct_trivia_format(trivia)
            filepath, filename = append_data_to_file(
                trivia_data,
                f"{trivia.get('category')}{settings.TRIVIA_FILES_SUFFIX}.json"
            )

            resource_file_relation = ResourceFileRelation(
                resource_id=created_resources.get(category)[0],
                filepath=filepath,
                filename=filename
            )

            resource_file_storage.append(resource_file_relation)

        upload_files_to_resources(resource_file_storage)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
