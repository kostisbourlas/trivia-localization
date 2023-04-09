from typing import Optional, Set

from localization.interface import TransifexAPI
from localization.objects import ResourceFileRelation, Resource
from localization.utils import (
    create_random_prefix,
    remove_files,
    category_exists_in_resources,
    append_data_to_file
)


def construct_trivia_format(trivia: dict) -> dict:
    prefix: str = create_random_prefix()
    trivia_format = {
        f"{prefix}question": trivia.get("question"),
        f"{prefix}correct_answer": trivia.get("correct_answer"),
    }

    for index, answer in enumerate(trivia.get("incorrect_answers")):
        trivia_format.update({f"{prefix}incorrect_answer_{index}": answer})

    return trivia_format


def get_resource_existing_data(resource_id: str) -> dict:
    return TransifexAPI.get_resource_data(resource_id)


def upload_files_to_resources(file_mapper: Set[ResourceFileRelation]):
    for item in file_mapper:
        existing_data: dict = get_resource_existing_data(item.resource_id)
        filepath, filename = append_data_to_file(existing_data, item.filename)
        with open(filepath, "rb") as file:
            TransifexAPI.upload_file_to_resource(
                file, filename, item.resource_id
            )
            _ = remove_files(item.filepath)


def get_created_resources() -> Set[Resource]:
    results: dict = TransifexAPI.get_all_resources().get("data")

    created_resources: Set[Resource] = set()
    if results:
        for item in results:
            resource = Resource(
                resource_id=item.get("id"),
                name=item.get("attributes").get("name"),
                slug=item.get("attributes").get("slug")
            )
            created_resources.add(resource)

    return created_resources


def get_resource_from_storage(
    category: str, storage: Set[Resource]
) -> Optional[Resource]:
    for resource in storage:
        if resource.name == category:
            return resource


def get_or_create_resource(category, resource_storage) -> Resource:
    # Check if a resource for the category exists in storage,
    # and create it if it doesn't
    if category_exists_in_resources(category, resource_storage):
        resource: Resource = get_resource_from_storage(
            category, resource_storage
        )
    else:
        response = TransifexAPI.create_resource(category)
        resource = Resource(
            resource_id=response.get("data").get("id"),
            name=response.get("data").get("attributes").get("name"),
            slug=response.get("data").get("attributes").get("slug")
        )
    return resource
