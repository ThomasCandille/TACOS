# Documentation - query_utils.py

## Table des Matières
- [Aperçu du Fichier](#aperçu-du-fichier)
- [Fonctionnalités Principales](#fonctionnalités-principales)
- [Dépendances & Imports](#dépendances--imports)
- [Structure du Code](#structure-du-code)
- [Exemples d'Utilisation](#exemples-dutilisation)
- [Configuration & Paramètres](#configuration--paramètres)
- [Notes Techniques](#notes-techniques)
- [Maintenance & Développement](#maintenance--développement)

## Aperçu du Fichier

**Type :** Module Python utilitaire  
**Technologie :** Python 3.x avec requêtes HTTP REST  
**Position :** Couche d'accès aux données dans l'architecture TACOS  
**Rôle :** Interface de communication avec l'API Mathis/Dremio pour l'authentification et l'exécution de requêtes SQL sur la base de données ANIS

### Description
Le fichier [`query_utils.py`](../query_utils.py) constitue la couche d'abstraction entre l'application TACOS et l'API REST Mathis. Il gère l'authentification utilisateur via NNI/mot de passe, l'obtention de tokens d'autorisation, et l'exécution asynchrone de requêtes SQL avec gestion des résultats paginés.

## Fonctionnalités Principales

### Système d'Authentification
- **Connexion sécurisée** : Authentification via API REST avec NNI et mot de passe
- **Gestion des tokens** : Récupération et formatage des tokens d'autorisation
- **Validation des credentials** : Retour de codes d'erreur explicites pour les échecs d'authentification

```python
def get_headers(nni, mdp):
    AUTH_DATA = {"userName": f"{nni}", "password": f"{mdp}"}
    r = requests.post("https://" + SERVER_HOST_ADDR + "/apiv2/login", 
                      data=json.dumps(AUTH_DATA), 
                      verify=USE_SSL_VERIFICATION, 
                      headers={"content-type": "application/json"})
```

### Exécution de Requêtes SQL Asynchrones
- **Soumission de jobs** : Envoi de requêtes SQL à l'API Dremio
- **Polling de statut** : Surveillance du statut d'exécution avec attente active
- **Récupération de résultats** : Gestion des réponses avec pagination automatique

```python
def make_query(query, headers):
    payload = {"sql": f"{query}"}
    r = requests.post("https://" + SERVER_HOST_ADDR + "/api/v3/sql", 
                      data=json.dumps(payload), 
                      verify=USE_SSL_VERIFICATION, 
                      headers=headers)
    jobId = r.json()["id"]
```

### Gestion des Résultats Paginés
- **Pagination automatique** : Récupération de résultats par lots de 500
- **Agrégation transparente** : Consolidation automatique des résultats multi-pages
- **Optimisation mémoire** : Traitement séquentiel pour les gros volumes de données

```python
# Gestion pagination avec limite de 500 résultats par page
offset = 0
limit = 500
results = []
while True:
    r = requests.get(f"https://{SERVER_HOST_ADDR}/api/v3/job/{jobId}/results?limit={limit}&offset={offset}", 
                     verify=USE_SSL_VERIFICATION, headers=headers)
    data = r.json()
    results.extend(data["rows"])
    if len(data["rows"]) < limit:
        break
    offset += limit
```

## Dépendances & Imports

### Bibliothèques Standard Python
```python
import requests   # Client HTTP pour communication REST API
import json      # Sérialisation/désérialisation JSON
import time      # Gestion des délais d'attente (polling)
import urllib3   # Désactivation des warnings SSL
```

### Intégration avec l'Écosystème TACOS
- **[script.py](../script.py)** : Utilisation principale pour récupération de données
- **[query.py](../query.py)** : Définition des requêtes SQL métier
- **API Mathis/Dremio** : Service d'authentification et d'exécution SQL RTE

### Configuration d'Environnement
- **Serveur de production / public** : `mathis.rte-france.com`
- **Serveur d'intégration** : `mathis-integration.rte-france.com`
- **SSL** : Vérification désactivée (`USE_SSL_VERIFICATION = False`)
- **Base de données** : ANIS (données opérationnelles RTE)

## Structure du Code

### Architecture Modulaire
```python
# 1. Configuration globale
SERVER_HOST_ADDR = "mathis.rte-france.com"
USE_SSL_VERIFICATION = False

# 2. Fonction d'authentification
def get_headers(nni, mdp) -> [headers, status_code_response]

# 3. Fonction d'exécution de requêtes
def make_query(query, headers) -> results
```

### Flux d'Authentification
1. **Préparation des données** : Formatage des credentials en JSON
2. **Appel API login** : POST vers `/apiv2/login`
3. **Validation du statut** : Contrôle des codes de retour HTTP
4. **Extraction du token** : Récupération depuis la réponse JSON
5. **Formatage des headers** : Constitution des en-têtes d'autorisation

### Flux d'Exécution de Requêtes
1. **Soumission** : POST de la requête SQL vers `/api/v3/sql`
2. **Récupération Job ID** : Extraction de l'identifiant de job
3. **Polling** : Surveillance du statut avec boucle d'attente
4. **États possibles** : `RUNNING` → `COMPLETED` / `FAILED` / `CANCELED`
5. **Récupération résultats** : GET paginé avec gestion des offsets

### Mécanismes de Gestion d'Erreurs
```python
# Gestion des erreurs d'authentification
if status_code != 200:
    headers = None
    if status_code in [401, 403, 404]:
        status_code_response = (status_code, f'{status_code} --> {r.reason}')
    else:
        status_code_response = (000, 'Erreur inconnue')

# Gestion des échecs d'exécution
if r.json()["jobState"] == "FAILED":
    results = None
```

## Exemples d'Utilisation

### Authentification Standard
```python
from query_utils import get_headers, make_query

# Connexion utilisateur
nni = "123456"
mdp = "motdepasse"
headers, response_tuple = get_headers(nni, mdp)

if headers is None:
    print(f"Erreur d'authentification: {response_tuple}")
else:
    print("Connexion réussie")
```

### Exécution de Requêtes Métier
```python
from query import query_to_get_gmr
from query_utils import make_query

# Récupération des GMR disponibles
query = query_to_get_gmr()
result = make_query(query, headers)

# Traitement des résultats
li_gmr = []
for gmr in result:
    li_gmr.append(gmr['GMR'])
```

### Workflow Complet dans script.py
```python
# Dans get_data() - Authentification lors de la connexion
@eel.expose
def get_data(nni, mdp):
    global headers
    headers, response_tuple = get_headers(nni, mdp)
    if headers is None:
        eel.display_error(response_tuple)
    else:
        eel.go_to('./pages/filters.html')

# Dans get_gmr() - Requête de données
@eel.expose  
def get_gmr():
    query = query_to_get_gmr()
    result = make_query(query, headers)
    li_gmr = [gmr['GMR'] for gmr in result]
    eel.display_gmr(li_gmr)
```

### Gestion des Requêtes Complexes
```python
# Requête avec filtres et jointures multiples
from query import query_to_get_og_ni

gmr = "GMR_NORD"
date_start = "2024-01-01" 
date_end = "2024-12-31"

query = query_to_get_og_ni(date_end, date_start, gmr)
og_ni_results = make_query(query, headers)

# Traitement des résultats volumineux (pagination automatique)
print(f"Récupéré {len(og_ni_results)} opérations")
```

## Configuration & Paramètres

### Paramètres de Serveur
```python
# Configuration production par défaut
SERVER_HOST_ADDR = "mathis.rte-france.com"

# Alternative intégration (commentée)
# SERVER_HOST_ADDR = "mathis-integration.rte-france.com"
```

### Configuration SSL et Sécurité
```python
USE_SSL_VERIFICATION = False  # Désactivation vérification certificats

# Suppression des warnings SSL
urllib3.disable_warnings()
```

### Paramètres de Pagination
```python
# Dans make_query() - Configuration des limites
offset = 0        # Point de départ pour pagination
limit = 500       # Nombre maximum de résultats par page
```

### Paramètres de Polling
```python
# Délai d'attente entre vérifications de statut
time.sleep(0.4)   # 400ms entre chaque vérification
```

### Endpoints API
```python
# Authentification
LOGIN_ENDPOINT = "/apiv2/login"

# Exécution SQL
SQL_ENDPOINT = "/api/v3/sql"

# Surveillance de jobs
JOB_STATUS_ENDPOINT = "/api/v3/job/{jobId}"

# Récupération de résultats
RESULTS_ENDPOINT = "/api/v3/job/{jobId}/results"
```

## Notes Techniques

### Considérations de Performance
- **Polling optimisé** : Délai de 400ms pour équilibrer réactivité/charge serveur
- **Pagination efficace** : Traitement par lots de 500 pour optimiser mémoire
- **Connexion persistante** : Réutilisation des headers d'authentification
- **Traitement asynchrone** : Architecture non-bloquante avec surveillance d'état

### Mesures de Sécurité
```python
# Authentification par token temporaire
TOKEN = r.json()["token"]
headers = {'Authorization': '_dremio{authToken}'.format(authToken=TOKEN)}

# Gestion sécurisée des credentials
AUTH_DATA = {"userName": f"{nni}", "password": f"{mdp}"}
# Pas de stockage persistant des mots de passe
```

### Limitations Connues
- **SSL désactivé** : Vérification de certificats désactivée (environnement interne)
- **Timeout non configuré** : Pas de limite de temps explicite pour les requêtes
- **Gestion d'erreurs basique** : Messages d'erreur limités
- **Pas de retry automatique** : Aucune logique de nouvelle tentative

### Optimisations Appliquées
```python
# Pagination intelligente - arrêt automatique
if len(data["rows"]) < limit:
    break  # Plus de données à récupérer

# Extension dynamique des résultats
results.extend(data["rows"])  # Plus efficace que append multiple

# Polling avec surveillance d'état
while r.json()["jobState"] == "RUNNING":
    time.sleep(0.4)  # Évite la surcharge du serveur
```

### Patterns d'Architecture
- **Separation of Concerns** : Authentification séparée de l'exécution
- **Stateless Design** : Pas de stockage d'état entre appels
- **Error Handling** : Retours explicites pour gestion d'erreurs
- **Configuration externe** : Paramètres facilement modifiables

## Maintenance & Développement

### Extension pour Nouveaux Environnements
```python
# Ajout d'un serveur de développement
def get_server_config(environment):
    servers = {
        "prod": "mathis.rte-france.com",
        "integration": "mathis-integration.rte-france.com",
        "dev": "mathis-dev.rte-france.com"  # Nouveau
    }
    return servers.get(environment, servers["prod"])

SERVER_HOST_ADDR = get_server_config(os.getenv("TACOS_ENV", "prod"))
```

### Amélioration de la Gestion d'Erreurs
```python
import logging

def make_query(query, headers):
    try:
        logging.info(f"Exécution requête: {query[:100]}...")
        # ... logique existante
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur réseau: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Erreur parsing JSON: {e}")
        return None
```

### Ajout de Configuration de Timeout
```python
def make_query(query, headers, timeout=300):
    payload = {"sql": f"{query}"}
    r = requests.post("https://" + SERVER_HOST_ADDR + "/api/v3/sql", 
                      data=json.dumps(payload), 
                      verify=USE_SSL_VERIFICATION, 
                      headers=headers,
                      timeout=timeout)  # Ajout timeout
```

### Tests Unitaires Recommandés
```python
import unittest
from unittest.mock import patch, Mock

class TestQueryUtils(unittest.TestCase):
    
    @patch('requests.post')
    def test_get_headers_success(self, mock_post):
        # Mock réponse succès
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"token": "test_token"}
        
        headers, response = get_headers("123456", "password")
        
        self.assertIsNotNone(headers)
        self.assertEqual(response[0], 0)
    
    @patch('requests.post')
    def test_get_headers_failure(self, mock_post):
        # Mock réponse échec
        mock_post.return_value.status_code = 401
        mock_post.return_value.reason = "Unauthorized"
        
        headers, response = get_headers("wrong", "credentials")
        
        self.assertIsNone(headers)
        self.assertEqual(response[0], 401)
```

### Debugging et Monitoring
```python
# Ajout de logs détaillés
def make_query(query, headers):
    start_time = time.time()
    logging.debug(f"Début exécution requête: {query}")
    
    # ... logique existante
    
    execution_time = time.time() - start_time
    logging.info(f"Requête exécutée en {execution_time:.2f}s - {len(results)} résultats")
    
    return results

# Monitoring des performances
def log_query_performance(query, execution_time, result_count):
    with open("query_performance.log", "a") as f:
        f.write(f"{datetime.now()},{len(query)},{execution_time},{result_count}\n")
```

### Guidelines de Contribution
1. **Sécurité** : Ne jamais logger les credentials ou tokens
2. **Performance** : Maintenir la pagination pour les gros volumes
3. **Robustesse** : Ajouter des try/catch pour les appels réseau
4. **Configuration** : Externaliser les paramètres d'environnement
5. **Logging** : Ajouter des logs appropriés sans données sensibles
6. **Tests** : Mocker les appels réseau pour les tests unitaires

### Fichiers Associés à Modifier
- **[script.py](../script.py)** : Utilisation principale des fonctions
- **[query.py](../query.py)** : Définition des requêtes SQL
- **Configuration** : Variables d'environnement pour serveurs
- **Tests** : Création de test_query_utils.py
- **Logs** : Configuration du système de logging