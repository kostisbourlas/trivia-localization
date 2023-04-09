# The file maps all the relevant Trasifex APIs.

from transifex_client import settings
from transifex_client.utils import slugify_string, call_url_post
from transifex_client.api_data import get_new_resource_data


class TransifexClient:
    def create_resource(self, name: str):
        data: dict = get_new_resource_data(name, slugify_string(name))
        headers: dict = {
            "Authorization": f"Bearer {settings.TRANSIFEX_SECRET_KEY}",
            "Content-Type": "application/vnd.api+json"
        }
        response: dict = call_url_post(
            settings.TRANSIFEX_RESOURCES_URL, data, headers
        )

        return response
