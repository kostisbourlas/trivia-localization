from django.conf import settings
from django.core.management import BaseCommand

from localization.interface import get_trivias, create_resource, \
    get_all_resources
from localization.service import construct_trivia_format, \
    upload_files_to_resources
from localization.utils import append_data_to_file


def get_created_resources():
    resources: dict = get_all_resources().get("data")

    created_resources: dict[str, tuple] = {}
    if resources:
        for resource in resources:
            resource_id: str = resource.get("id")
            name: str = resource.get("attributes").get("name")
            slug: str = resource.get("attributes").get("slug")

            created_resources[name] = (resource_id, slug)

    return created_resources


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--categories", nargs="+", type=str)

    def handle(self, *args, **options):
        categories = set(options.get("categories"))

        created_resources: dict[str, tuple] = get_created_resources()

        filepath_resource_mapper: dict = {}
        for trivia in get_trivias(categories):
            category = trivia.get("category")
            if category not in created_resources:
                response = create_resource(category)
                resource_id = response.get("data").get("id")
                slug = response.get("data").get("attributes").get("slug")
                created_resources[category] = (resource_id, slug)
            else:
                resource_id = created_resources[category][0]

            trivia_data: dict = construct_trivia_format(trivia)
            filepath, filename = append_data_to_file(
                trivia_data,
                f"{trivia.get('category')}{settings.TRIVIA_FILES_SUFFIX}.json"
            )

            filepath_resource_mapper[resource_id] = (filepath, filename)

        upload_files_to_resources(filepath_resource_mapper)

        self.stdout.write(self.style.SUCCESS("Command successfully ran"))
