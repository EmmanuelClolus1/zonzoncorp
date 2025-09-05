import requests
from google.cloud import bigquery
import json
from utils import *
import pandas as pd
import pandas_gbq
import os 
from dotenv import load_dotenv

# Chargement des variables en .env
load_dotenv()

### ETAPE 1 --- Paramétrage & Query pour API Grid 

# Parametres API Grid GraphQL
graphql_url = "https://api-op.grid.gg/central-data/graphql"
api_key = os.getenv("API_KEY")

# Headers - Dict
headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key 
}

# Redaction de la Query pour GraphQL
graphql_query = """
    fragment organizationFields on Organization {
      id
      name
      teams {
        name
      }
    }

    query GetOrganizations {
      organizations(first: 5) {
        edges {
          node {
            ...organizationFields
          }
        }
      }
    }
"""

# Mise en place de la Query dans le PlayLoad
payload = {
    "query": graphql_query
}

# ETAPE 2 --- CALL API
try:
    # Request POST avec les parametres défini en ETAPE 1
    reponse = requests.post(graphql_url, headers=headers, json=payload)
    
    # Check ERROR
    # GraphQL renvoie tjrs 200 en code API -> L'erreur est dans le corps du JSON
    donnees_graphql = reponse.json()
    if 'errors' in donnees_graphql:
        print("Erreur de l'API GraphQL :")
        for erreur in donnees_graphql['errors']:
            print(erreur.get('message', 'Message d\'erreur non disponible.'))
        exit() # On arrête le script en cas d'erreur de requête

    #IMO USELESSSSSSSSSSSSSSS    
    # On vérifie les erreurs de statut HTTP (au cas où l'API renvoie autre chose qu'un 200)
    # reponse.raise_for_status()

# Erreur Réseau, hors ligne, timeout, SSL
except requests.exceptions.RequestException as e:
    print(f"Erreur de connexion HTTP : {e}")
    exit()

print(reponse)