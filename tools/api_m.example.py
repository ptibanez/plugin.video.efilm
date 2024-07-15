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
username = "28624546"
password = "190546"
login = api.login(username, password)
api.set_token(login["access"])
loans_actives = api.loans_actives()
loan = loans_actives[0]
#loan = api.loan(loan_id)
#loan_displays = api.loan_displays(loan_id)
product_id = loan["product"]
product_type = loan["product_type"]
if product_type == "audiovisual": 
    info = api.videos_audiovisuals(product_id)

prettyPrint(info)

#print(info)
       

