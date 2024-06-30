# flake8: noqa
import json
import sys
import os

PARENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_PATH)  # Add parent path to searchable list
from resources.lib.api import Api


def prettyPrint(data):
    print(json.dumps(data, indent=2))


DOMAIN = "ANDALUCÍA.EFILM Red de Bibliotecas Públicas de Andalucía"

api = Api(DOMAIN)

# .. You can keep testing the api here
prettyPrint(api.collections())
