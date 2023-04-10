# The file maps all the relevant Trasifex APIs.
from typing import Optional

from transifex_client import settings
from transifex_client.utils import (
    slugify_string, call_url_post,
    call_url_post_with_files,
    call_url_get
)
from transifex_client.payload import (
    construct_resources_payload,
    get_request_resource_data_payload
)


class TransifexClient:
    def get_all_resources(self):
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
        }
        response: dict = call_url_get(settings.TRANSIFEX_RESOURCES_URL, headers)
        return response

    def create_resource(self, name: str) -> dict:
        data: dict = construct_resources_payload(name, slugify_string(name))
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
        payload = {"resource": resource}
        files = {"content": (filename, file, "application/json")}
        response = call_url_post_with_files(
            settings.TRANSIFEX_UPLOAD_FILE_URL, files, headers, payload
        )
        return response

    def get_resource_data(self, resource_id) -> dict:
        request_id: Optional[str] = self._request_resource_download(resource_id)
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
        }
        response: dict = {}
        if request_id:
            response: dict = call_url_get(
                f"{settings.TRANSIFEX_REQUEST_RESOURCE_DATA_URL}/{request_id}",
                headers
            )

        return response

    def _request_resource_download(self, resource_id) -> Optional[str]:
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
            "Content-Type": "application/vnd.api+json"
        }
        payload: dict = get_request_resource_data_payload(resource_id)
        retries: int = 5
        while retries > 0:
            response: dict = call_url_post(
                settings.TRANSIFEX_REQUEST_RESOURCE_DATA_URL, payload, headers
            )
            retries -= 1
            if response.get("data").get("attributes").get("status") == "succeeded":
                return response.get("data").get("id")

        # Assume that status is still pending which occurs when the resource
        # has been created, but it contains no data.
        return None

    def get_request_file_upload_data(self, request_id: str):
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
        }
        response: dict = call_url_get(
            f"{settings.TRANSIFEX_UPLOAD_FILE_URL}/{request_id}", headers
        )

        return response
