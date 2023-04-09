from transifex_client import settings


def construct_resources_payload(name: str, slug: str) -> dict:
    return {
        "data": {
            "attributes": {
                "accept_translations": True,
                "name": name,
                "priority": "normal",
                "slug": slug
            },
            "relationships": {
                "i18n_format": {
                    "data": {
                        "id": "KEYVALUEJSON",
                        "type": "i18n_formats"
                    }
                },
                "project": {
                    "data": {
                        "id": settings.TRANSIFEX_ORG_PROJECT,
                        "type": "projects"
                    }
                }
            },
            "type": "resources"
        }
    }


def get_request_resource_data_payload(resource_id: str) -> dict:
    return {
        "data": {
            "attributes": {
                "callback_url": None,
                "content_encoding": "text",
                "file_type": "default",
                "pseudo": False,
                "pseudo_length_increase": 1
            },
            "relationships": {
                "resource": {
                    "data": {
                        "id": resource_id,
                        "type": "resources"
                    }
                }
            },
            "type": "resource_strings_async_downloads"
        }
    }
