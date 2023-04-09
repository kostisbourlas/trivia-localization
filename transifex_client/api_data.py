from transifex_client import settings


def get_new_resource_data(name: str, slug: str) -> dict:
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

