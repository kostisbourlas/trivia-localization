# This is the interface that will be used publicly from the other modules.

from transifex_client.transifex_client import TransifexClient


def create_resource(name: str) -> dict:
    client = TransifexClient()
    response = client.create_resource(name)
    return response


def get_all_resources() -> dict:
    client = TransifexClient()
    response = client.get_all_resources()
    return response


def upload_file_to_resource(file, filename: str, resource: str) -> dict:
    client = TransifexClient()
    response = client.upload_file_to_resource(file, filename, resource)
    return response


def get_resource_data(resource_id: str) -> dict:
    client = TransifexClient()
    response = client.get_resource_data(resource_id)
    return response


def get_request_file_upload_data(request_id: str):
    client = TransifexClient()
    response = client.get_request_file_upload_data(request_id)
    return response
