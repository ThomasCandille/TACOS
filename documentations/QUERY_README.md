# Documentation - query.py

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

**Type :** Module Python de requêtes SQL  
**Technologie :** Python 3.x avec requêtes SQL pour base de données Dremio  
**Position :** Couche d'accès aux données dans l'architecture TACOS  
**Rôle :** Définit et centralise toutes les requêtes SQL métier pour l'extraction des données opérationnelles depuis la base de données ANIS

### Description
Le fichier [`query.py`](../query.py) constitue le référentiel centralisé de toutes les requêtes SQL utilisées dans l'application TACOS. Il contient les requêtes complexes pour extraire les données des Opérations Globales (OG), Notes d'Information (NI), équipes intervenantes et autres entités métier depuis la base de données ANIS via l'API Dremio.

## Fonctionnalités Principales

### Requêtes de Récupération des Données de Base
- **GMR** : Extraction de la liste complète des GMR disponibles
- **Opérations Globales et Notes d'Information** : Récupération filtrée par période et GMR
- **Équipes pilotes et intervenantes** : Extraction des codes d'équipes par contexte

### Requêtes Métier Spécialisées
- **Recherche par identifiants** : Conversion entre numéros OG/NI et IDs techniques
- **Données d'intervention** : Extraction complète des informations d'opération pour génération Excel
- **Jointures complexes** : Agrégation de données depuis multiple tables liées

```python
def query_to_get_og_ni(date_end, date_start, gmr):
    # Requête complexe avec jointures multiples et filtres temporels
    return f"SELECT TB025_OPERATION_GLOBALE.NUMERO_OG, TB001_NOTE_INFORMATION.NUMERO_NI, ..."

def query_get_operation_intervention(operation):
    # Extraction complète des données d'intervention avec dernier indice
    return f"SELECT TB004_OPERATION_UNITAIRE.ID_OU, ..., TB002_INDICE.NUMERO_INDICE ..."
```

### Fonctions d'Accès aux Données
```python
# 1. Données de référence
query_to_get_gmr()                          # Liste des GMR
query_get_equipes_pilotes(gmr)              # Équipes pilotes par GMR
query_get_equipes_intervenantes(numero_ni)  # Équipes d'une NI spécifique

# 2. Recherche d'opérations
query_to_get_og_ni(date_end, date_start, gmr)  # OG/NI par période et GMR
query_get_operation_intervention(operation)     # Détails d'intervention

# 3. Conversions d'identifiants
query_get_id_og_from_numero_og(numero_og)   # OG numéro → ID technique
query_get_id_og_from_numero_ni(numero_ni)   # NI numéro → ID technique
```

## Dépendances & Imports

### Aucune Dépendance Externe
Le module `query.py` est entièrement autonome et ne contient que des fonctions Python pures retournant des chaînes SQL.

### Intégration avec l'Écosystème TACOS
- **[script.py](../script.py)** : Utilisation principale des requêtes pour génération Excel
- **[query_utils.py](../query_utils.py)** : Exécution des requêtes via `make_query()`
- **Base ANIS** : Cible des requêtes via l'API Dremio/Mathis

### Architecture de Base de Données
```sql
-- Base de données production
-- "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TBxxx"

-- Base de données intégration (commentée)
-- "PUBLIC".ANIS."REC_ANIS".ANIS."TBxxx"

-- Base de données publique (alternative)
"PUBLIC".ANIS."TBxxx"
```

## Structure du Code

### Organisation Fonctionnelle par Type de Données
```python
# 1. Données de référence (GMR, équipes)
query_to_get_gmr()
query_get_equipes_pilotes(gmr)
query_get_equipes_intervenantes(numero_ni)

# 2. Recherche d'opérations complexes
query_to_get_og_ni(date_end, date_start, gmr)
query_get_operation_intervention(operation)

# 3. Utilitaires de conversion d'IDs
query_get_id_og_from_numero_og(numero_og)
query_get_id_og_from_numero_ni(numero_ni)
```

### Architecture des Requêtes Complexes

#### Jointures Multi-Tables
```sql
-- Exemple dans query_to_get_og_ni()
FROM TB001_NOTE_INFORMATION 
LEFT JOIN TB005_NI_OU ON TB001_NOTE_INFORMATION.ID_NI = TB005_NI_OU.ID_NI
LEFT JOIN TB004_OPERATION_UNITAIRE ON TB005_NI_OU.ID_OU = TB004_OPERATION_UNITAIRE.ID_OU
LEFT JOIN TB007_OUVRAGE ON TB004_OPERATION_UNITAIRE.ID_OUVRAGE = TB007_OUVRAGE.ID_OUVRAGE
-- ... (8 jointures supplémentaires)
```

#### Filtres Métier Sophistiqués
```sql
-- Filtrage temporel avec chevauchement de périodes
WHERE NOT (TB001_NOTE_INFORMATION.DATE_DEB_NI > TO_DATE('{date_end}','YYYY-MM-DD') 
           OR TB001_NOTE_INFORMATION.DATE_FIN_NI < TO_DATE('{date_start}','YYYY-MM-DD'))

-- Exclusion des opérations isolées (minimum 2 OU par OG)
AND TB025_OPERATION_GLOBALE.NUMERO_OG IN (
    SELECT NUMERO_OG FROM ... GROUP BY NUMERO_OG HAVING COUNT(ALL NUMERO_OG) > 1
)
```

### Pattern d'Injection de Paramètres
Toutes les fonctions utilisent des f-strings pour l'injection sécurisée de paramètres dans les requêtes SQL.

## Exemples d'Utilisation

### Récupération des GMR Disponibles
```python
from query import query_to_get_gmr
from query_utils import make_query

# Dans script.py - Fonction get_gmr()
query = query_to_get_gmr()
result = make_query(query, headers)
li_gmr = [gmr['GMR'] for gmr in result]
```

### Recherche d'Opérations par Critères
```python
from query import query_to_get_og_ni

# Paramètres de recherche
gmr = "GMR_NORD"
date_start = "2024-01-01"
date_end = "2024-12-31"

# Exécution de la requête
query = query_to_get_og_ni(date_end, date_start, gmr)
og_ni_results = make_query(query, headers)

# Traitement des résultats
for operation in og_ni_results:
    print(f"OG: {operation['NUMERO_OG']}, NI: {operation['NUMERO_NI']}")
```

### Extraction des Données d'Intervention Complètes
```python
from query import query_get_operation_intervention, query_get_id_og_from_numero_og

# Conversion numéro → ID technique
numero_og = "OG-2024-0001"
id_og_query = query_get_id_og_from_numero_og(numero_og)
id_og = make_query(id_og_query, headers)[0]['ID_OG']

# Extraction des données d'intervention
intervention_query = query_get_operation_intervention(id_og)
result = make_query(intervention_query, headers)

# Données prêtes pour génération Excel
for row in result:
    print(f"OU: {row['LIBELLE_OU']}, Équipe: {row['CODE_TB17']}")
```

### Récupération des Équipes Contextuelles
```python
from query import query_get_equipes_pilotes, query_get_equipes_intervenantes

# Équipes pilotes du GMR
equipes_pilotes_query = query_get_equipes_pilotes("GMR_NORD")
equipes_pilotes = make_query(equipes_pilotes_query, headers)

# Équipes intervenantes sur une NI spécifique
equipes_ni_query = query_get_equipes_intervenantes("NI-2024-0001")
equipes_ni = make_query(equipes_ni_query, headers)
```

## Configuration & Paramètres

### Schémas de Base de Données
```python
# Configuration publique (par défaut)
PROD_SCHEMA = '"PUBLIC".ANIS."TBxxx"'

# Alternatives disponibles (commentées dans le code)
# INTEGRATION_SCHEMA = '"PUBLIC".ANIS."REC_ANIS".ANIS."TBxxx"'
# PRODUCTION_SCHEMA = '"PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TBxxx"'
```

### Tables de la Base ANIS Utilisées
```python
# Tables principales
TB001_NOTE_INFORMATION          # Notes d'information
TB002_INDICE                   # Indices de version
TB004_OPERATION_UNITAIRE       # Opérations unitaires
TB005_NI_OU                    # Liaison NI ↔ OU
TB007_OUVRAGE                  # Ouvrages du réseau
TB009_GMR                      # Groupes de Maintenance Régionaux
TB014_GDP                      # Groupes de Dispatching
TB015_OUVRAGE_GDP              # Liaison Ouvrage ↔ GDP
TB017_PARTIE_PRENANTE_RGPD     # Parties prenantes
TB018_OU_PP                    # Liaison OU ↔ Partie Prenante
TB020_NI_PP                    # Liaison NI ↔ Partie Prenante
TB023_EQUIPE_RGPD              # Équipes
TB025_OPERATION_GLOBALE        # Opérations globales
```

### Paramètres de Filtrage Métier
```python
# Filtres de validation dans query_get_equipes_intervenantes()
TYPE_EXCLUSIONS = ["Client"]              # Types de parties prenantes à exclure
NOM_EXCLUSIONS = ["%COSE%"]              # Motifs de noms à exclure

# Format de dates attendu
DATE_FORMAT = "YYYY-MM-DD"               # Format pour TO_DATE()
```

### Critères de Sélection d'Opérations
```python
# Dans query_to_get_og_ni() - Conditions métier
MIN_OPERATIONS_PER_OG = 2                # Minimum d'OU par OG
TEMPORAL_OVERLAP_LOGIC = True            # Logique de chevauchement de périodes
GMR_PARTIAL_MATCH = True                 # Correspondance partielle GMR (LIKE '%{gmr}%')
```

## Notes Techniques

### Optimisations de Performance
- **Jointures LEFT JOIN** : Préservation des données même en cas de liaisons manquantes
- **Indexation implicite** : Utilisation des clés primaires et étrangères pour optimisation
- **Filtrage précoce** : Conditions WHERE appliquées avant les agrégations
- **Pagination gérée** : Par `query_utils.py` (limite de 500 résultats par page)

### Gestion des Cas Limites
```sql
-- Gestion des périodes chevauchantes
NOT (date_debut > fin_periode OR date_fin < debut_periode)

-- Récupération du dernier indice uniquement
TB002_INDICE.NUMERO_INDICE IN (SELECT MAX(NUMERO_INDICE) FROM ...)

-- Exclusion des données manquantes
WHERE TB009_GMR.LIBELLE LIKE '%{gmr}%'  -- Tolérance de correspondance partielle
```

### Patterns d'Architecture SQL
- **Star Schema** : Architecture en étoile avec table centrale et dimensions
- **Slowly Changing Dimensions** : Gestion des versions via TB002_INDICE
- **Referential Integrity** : Jointures strictes sur les clés étrangères
- **Temporal Queries** : Filtrage par plages de dates avec logique de chevauchement

### Considérations de Sécurité
```python
# Injection SQL préventive via f-strings contrôlées
# Paramètres validés côté application avant injection
def query_to_get_og_ni(date_end, date_start, gmr):
    # Les paramètres sont supposés pré-validés par l'appelant
    return f"... WHERE date BETWEEN '{date_start}' AND '{date_end}' ..."
```

## Maintenance & Développement

### Ajout de Nouvelles Requêtes
```python
def query_nouvelle_fonctionnalite(param1, param2):
    """
    Description de la nouvelle requête
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
    
    Returns:
        str: Requête SQL formatée
    """
    return f"""
        SELECT colonne1, colonne2
        FROM "PUBLIC".ANIS."TB_NOUVELLE"
        WHERE condition1 = '{param1}' AND condition2 = '{param2}'
    """
```

### Modification des Schémas
```python
# Pour basculer vers l'environnement d'intégration
def get_table_path(environment="prod"):
    schemas = {
        "prod": '"PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS',
        "integration": '"PUBLIC".ANIS."REC_ANIS".ANIS',
        "public": '"PUBLIC".ANIS'
    }
    return schemas.get(environment, schemas["prod"])

def query_to_get_gmr(environment="prod"):
    schema = get_table_path(environment)
    return f'SELECT DISTINCT TB009_GMR.LIBELLE AS GMR FROM {schema}."TB009_GMR"'
```

### Tests et Validation
```python
# Tests recommandés pour validation des requêtes
def test_query_syntax():
    """Vérification syntaxe SQL de base"""
    queries = [
        query_to_get_gmr(),
        query_to_get_og_ni("2024-12-31", "2024-01-01", "TEST_GMR"),
        # ... autres requêtes
    ]
    for query in queries:
        assert isinstance(query, str)
        assert "SELECT" in query.upper()

def test_query_parameters():
    """Validation injection de paramètres"""
    query = query_to_get_og_ni("2024-12-31", "2024-01-01", "GMR_TEST")
    assert "2024-12-31" in query
    assert "2024-01-01" in query
    assert "GMR_TEST" in query
```

### Debugging des Requêtes
```python
# Ajout de logging pour debugging
import logging

def query_to_get_og_ni(date_end, date_start, gmr):
    query = f"SELECT ... WHERE ... LIKE '%{gmr}%' ..."
    logging.debug(f"Requête OG/NI générée: {query[:200]}...")
    return query

# Validation des résultats côté script.py
result = make_query(query, headers)
logging.info(f"Requête retourne {len(result)} résultats")
```

### Guidelines de Contribution
1. **Nommage cohérent** : Préfixe `query_` + action + entité
2. **Documentation** : Docstring décrivant le but et les paramètres
3. **Validation paramètres** : Assume validation côté appelant
4. **Performance** : Privilégier jointures LEFT JOIN pour robustesse
5. **Schéma uniforme** : Utiliser le schéma de production par défaut
6. **Formatage** : SQL indenté et lisible avec f-strings

### Fichiers Associés à Modifier
- **[script.py](../script.py)** : Appels aux nouvelles requêtes
- **[query_utils.py](../query_utils.py)** : Aucune modification nécessaire (générique)
- **Tests** : Création de test_query.py pour validation
- **Documentation** : Mise à jour du schéma de base de données