import os

from dotenv import load_dotenv

load_dotenv()

TRANSIFEX_SECRET_KEY = os.getenv("TRANSIFEX_SECRET_KEY")
TRANSIFEX_ORG_PROJECT = "o:koboucompany:p:assignment-trivia"

# Trasifex URLS
TRANSIFEX_BASE_URL = "https://rest.api.transifex.com"
TRANSIFEX_RESOURCES_URL = f"{TRANSIFEX_BASE_URL}/resources?filter[project]={TRANSIFEX_ORG_PROJECT}"
TRANSIFEX_UPLOAD_FILE_URL = f"{TRANSIFEX_BASE_URL}/resource_strings_async_uploads"
TRANSIFEX_REQUEST_RESOURCE_DATA_URL = f"{TRANSIFEX_BASE_URL}/resource_strings_async_downloads"
