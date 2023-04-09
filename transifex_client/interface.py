# This is the interface that will be used publicly from the other modules.

from transifex_client.transifex_client import TransifexClient


def create_resource(name: str):
    client = TransifexClient()
    response = client.create_resource(name)
    return response
