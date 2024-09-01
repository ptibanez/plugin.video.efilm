# flake8: noqa
import json
import sys
import os
import requests
import logging
import sys


PARENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(PARENT_PATH)  # Add parent path to searchable list
from resources.lib.api import Api
logging.basicConfig(stream=sys.stdout, level=logging.NOTSET)

def prettyPrint(data):
    print(json.dumps(data, indent=2))


DOMAIN = "ANDALUCÍA.EFILM Red de Bibliotecas Públicas de Andalucía"

api = Api(DOMAIN)

# .. You can keep testing the api here
username = ""
password = ""
login = api.login(username, password)
api.set_token(login["access"])
loans = api.loans_actives()
pelicula = loans[0]
print("\nPelícula:")
prettyPrint(pelicula)
#serie = loans[1]
#print("\nSerie:")
#prettyPrint(serie)
pelicula_info = api.videos_audiovisuals(pelicula["product"])
print("\nPelícula -> info:")
prettyPrint(pelicula_info)
#serie_info = api.videos_series(serie["collection_id"])
#print("\nSerie -> info:")
#prettyPrint(serie_info)


       

