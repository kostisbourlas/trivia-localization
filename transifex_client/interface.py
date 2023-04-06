# This is the interface that will be used publicly from the other modules.

from transifex_client.transifex_client import TransifexClient


def upload_resource():
    client = TransifexClient()
    response = client.upload_resource()
    return response
