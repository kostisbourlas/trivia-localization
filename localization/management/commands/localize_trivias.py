from typing import List, Set

from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import TriviaAPI, TransifexAPI
from localization.objects import ResourceFileRelation, Resource
from localization.service import (
    construct_trivia_format,
    upload_files_to_resources,
    get_created_resources,
    get_resource_from_storage
)
from localization.utils import append_data_to_file, category_exists_in_resources


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        resource_storage: Set[Resource] = get_created_resources()

        resource_file_storage: Set[ResourceFileRelation] = set()
        for trivia in TriviaAPI.get_trivias(categories):
            category = trivia.get("category")

            if not category_exists_in_resources(category, resource_storage):
                response = TransifexAPI.create_resource(category)
                resource = Resource(
                    resource_id=response.get("data").get("id"),
                    name=response.get("data").get("attributes").get("name"),
                    slug=response.get("data").get("attributes").get("slug")
                )
                resource_storage.add(resource)
            else:
                resource: Resource = get_resource_from_storage(
                    category, resource_storage
                )

            trivia_data: dict = construct_trivia_format(trivia)
            filepath, filename = append_data_to_file(
                trivia_data,
                f"{trivia.get('category')}{settings.TRIVIA_FILES_SUFFIX}.json"
            )

            resource_file_relation = ResourceFileRelation(
                resource_id=resource.resource_id,
                filepath=filepath,
                filename=filename
            )

            resource_file_storage.add(resource_file_relation)

        upload_files_to_resources(resource_file_storage)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
