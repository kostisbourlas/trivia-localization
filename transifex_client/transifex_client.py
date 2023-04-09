# The file maps all the relevant Trasifex APIs.
import os

from dotenv import load_dotenv

load_dotenv()

TRANSIFEX_SECRET_KEY = os.getenv('TRANSIFEX_SECRET_KEY')


class TransifexClient:
    def upload_resource(self):
        return NotImplemented

    def create_resource(self):
        pass
