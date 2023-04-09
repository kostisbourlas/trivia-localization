from typing import Set

from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import TriviaAPI
from localization.objects import ResourceFileRelation, Resource
from localization.service import (
    construct_trivia_format,
    upload_files_to_resources,
    get_created_resources,
    get_or_create_resource
)
from localization.utils import append_data_to_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        # Get a set of created resources from project
        resource_storage: Set[Resource] = get_created_resources()

        # Create a set to hold resource-file relations
        resource_file_storage: Set[ResourceFileRelation] = set()

        # Iterate over the results from TriviaAPI for the specified categories
        for trivia in TriviaAPI.get_trivias(categories):
            category = trivia.get("category")

            resource: Resource = get_or_create_resource(
                category, resource_storage
            )
            resource_storage.add(resource)

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
