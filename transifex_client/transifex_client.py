# The file maps all the relevant Trasifex APIs.

from transifex_client import settings
from transifex_client.utils import (
    slugify_string, call_url_post,
    call_url_post_with_files
)
from transifex_client.api_data import get_new_resource_data


class TransifexClient:
    def create_resource(self, name: str) -> dict:
        data: dict = get_new_resource_data(name, slugify_string(name))
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
            "Content-Type": "application/vnd.api+json"
        }
        response: dict = call_url_post(
            settings.TRANSIFEX_RESOURCES_URL, data, headers
        )
        return response

    def upload_file_to_resource(self, file, filename, resource: str) -> dict:
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
        }
        payload = {'resource': resource}
        files = {
            "content": (
                filename,
                file,
                "application/json",
            ),
        }
        response = call_url_post_with_files(
            settings.TRANSIFEX_UPLOAD_FILE_URL, files, headers, payload
        )
        print(response)
        return response
