import functools
from typing import Set, Optional

from django.conf import settings

from localization.interface import TransifexAPI, TriviaAPI
from localization.objects import ResourceFileRelation, Resource
from localization.utils import (
    create_random_prefix,
    remove_files,
    category_exists_in_resources,
    append_data_to_file,
    get_resource_from_storage,
    call_url_with_polling
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


def process_files_to_upload(
    file_mapper: Set[ResourceFileRelation]
) -> Set[ResourceFileRelation]:
    failed_uploads: Set[ResourceFileRelation] = set()

    for item in file_mapper:
        failed_upload: ResourceFileRelation = process_file_to_upload(item)
        if failed_upload:
            failed_uploads.add(failed_upload)

    return failed_uploads


def process_file_to_upload(
    item: ResourceFileRelation
) -> Optional[ResourceFileRelation]:
    """
    Gets existing data from the resource, appends them to the prepared json
    file and push them into Transifex. Then, it polls for a response and depends
    on the status either removes the files or appends them into a data structure
    in order to be pushed again in the future
    :param item: A ResourceFileRelation
    :return: A ResourceFileRelation that represents the failed upload or None in
    case the upload succeeded
    """
    # get existing data from the specified resource
    existing_data: dict = TransifexAPI.get_resource_data(item.resource_id)

    # append existing data to the new
    filepath, filename = append_data_to_file(existing_data, item.filename)

    with open(filepath, "rb") as file:
        # upload file to specific resource
        response = TransifexAPI.upload_file_to_resource(
            file, filename, item.resource_id
        )
        request_id: str = response.get("data").get("id")
        success_status: str = "succeeded"
        call_url: callable = functools.partial(
            TransifexAPI.get_request_file_upload_data, request_id=request_id
        )
        # poll for response
        response: dict = call_url_with_polling(
            call_url=call_url,
            retries=5,
            dict_path="data/attributes/status",
            message=success_status
        )
        status: str = response.get("data", "").get("attributes", "").get(
            "status", "")

        # either clear the files or leave them and register
        # the ResourceFileRelation for trying to upload them again
        if status == success_status:
            _ = remove_files(item.filepath)
            return None

    return item


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


def get_or_create_resource(
    resource: str, resource_storage: Set[Resource]
) -> Resource:
    """
    Checks if a resource exists in the Set and if it doesn't, call Transifex
    API to create it and store it to the Set
    :param resource: Str
    :param resource_storage: Set[Resource]
    :return: A Resource namedtuple object
    """
    if category_exists_in_resources(resource, resource_storage):
        resource_obj: Resource = get_resource_from_storage(
            resource, resource_storage
        )
    else:
        response = TransifexAPI.create_resource(resource)
        resource_obj = Resource(
            resource_id=response.get("data").get("id"),
            name=response.get("data").get("attributes").get("name"),
            slug=response.get("data").get("attributes").get("slug")
        )
    return resource_obj


def prepare_trivias_to_upload(categories: Set[str]) -> Set[ResourceFileRelation]:
    """
    Gets all resources from Transifex project. Iterates over the categories,
    creating new resources if needed and constructing the correct format that
    will be appending to the file in order to be pushed to the right resources
    :param categories: Set[str]
    :return: A Set[ResourceFileRelation] that will be iterated over to upload
    the relevant files to the right resources
    """
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

        # Create a resource-file relation that will be used to push the files
        # to the specific resource
        resource_file_relation = ResourceFileRelation(
            resource_id=resource.resource_id,
            filepath=filepath,
            filename=filename
        )
        resource_file_storage.add(resource_file_relation)
    return resource_file_storage
