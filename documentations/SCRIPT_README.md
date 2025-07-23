# Documentation - script.py

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

**Type :** Module Python principal avec serveur Eel intégré  
**Technologie :** Python 3.x avec framework Eel, xlwings, datetime  
**Position :** Serveur backend et point d'entrée principal de l'application TACOS  
**Rôle :** Orchestrateur central gérant l'authentification, la récupération de données, la logique métier et la génération de fiches Excel de coordination

### Description
Le fichier [`script.py`](../script.py) constitue le cœur de l'application TACOS. Il expose les fonctions Python via le framework Eel pour l'interface web, gère la communication avec la base de données ANIS, implémente la logique de validation des opérations et orchestre la génération automatisée de fiches Excel de coordination personnalisées.

## Fonctionnalités Principales

### Interface d'Authentification
- **Validation des credentials** : Authentification via NNI/mot de passe avec API Mathis
- **Gestion de session** : Stockage global des headers d'autorisation
- **Redirection automatique** : Navigation vers l'interface de filtres après connexion

```python
@eel.expose
def get_data(nni, mdp):
    global headers
    headers, response_tuple = get_headers(nni, mdp)
    if (headers is None):
        nni, mdp = "", ""
        eel.display_error(response_tuple)
    else:
        eel.go_to('./pages/filters.html')
```

### Récupération et Traitement des Données
- **Extraction des GMR** : Récupération de la liste complète des Groupes de Maintenance Régionaux
- **Filtrage des opérations** : Sélection OG/NI par période temporelle et GMR
- **Validation métier** : Application de règles de validation complexes
- **Optimisation des performances** : Traitement en lots avec mesure de temps d'exécution

```python
@eel.expose
def get_filters(gmr, date_start, date_end):
    global og, ni, main_gmr
    main_gmr = gmr
    start = time.time()
    
    # Récupération et filtrage des opérations
    query = query_to_get_og_ni(date_end, date_start, gmr)
    og_ni = make_query(query, headers)
    
    # Validation métier avec règles complexes
    for operation_globale in dic_operations_unique:
        query = query_get_equipes_intervenantes(...)
        list_equipe = make_query(query, headers)
        
        if is_operation_valid(dic_operations_unique[operation_globale], list_equipe):
            # Ajout à la liste avec formatage HTML
```

### Génération Automatisée d'Excel
- **Manipulation de template** : Ouverture et modification du fichier TEMPLATE.xlsm
- **Calculs temporels** : Gestion des calendriers avec années bissextiles
- **Application visuelle** : Couleurs conditionnelles par équipes
- **Sauvegarde intelligente** : Nommage automatique avec données contextuelles

```python
@eel.expose
def generate_excel(operation):
    # Récupération des données complètes d'intervention
    wb_obj = xw.Book(f"./_internal/TEMPLATE.xlsm")
    sheet = wb_obj.sheets['FicheDeCoordination']
    
    # Application des données métier
    sheet['A1'].value = f"Fiche De Coordination {data_row['NUMERO_NI']}"
    
    # Génération du calendrier avec couleurs
    for j in range(first_day_operation, last_day_operation, 1):
        sheet[f'{getColumn(j)}{index + (i - correct_i_value_for_excel)*2}'].color = background_color
```

## Dépendances & Imports

### Bibliothèques Standard Python
```python
import sys          # Gestion des chemins système et arguments
import time         # Mesure de performance et timing
import datetime     # Manipulation des dates et calendriers
import os           # Opérations sur le système de fichiers
```

### Frameworks et Bibliothèques Spécialisées
```python
import eel          # Framework web Python ↔ JavaScript
import xlwings as xw  # Manipulation des fichiers Excel
```

### Modules Internes du Projet
```python
from query import (
    query_to_get_gmr, query_to_get_og_ni, query_get_operation_intervention,
    query_get_equipes_pilotes, query_get_id_og_from_numero_og,
    query_get_id_og_from_numero_ni, query_get_equipes_intervenantes
)
from query_utils import make_query, get_headers
from function_utils import (
    get_background_color, get_operation_day_number, days_in_year,
    getColumn, is_operation_valid, isEquipeHere
)
```

### Configuration d'Environnement
- **Répertoire d'exécution** : Configuration dynamique des chemins
- **Template Excel** : `TEMPLATE.xlsm` dans `_internal/`
- **Répertoire de sortie** : `ficheExcel/` créé automatiquement
- **Interface web** : Dossier `web/` pour les ressources frontend

## Structure du Code

### Architecture Eel avec Fonctions Exposées
```python
# 1. Initialisation et configuration
exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0, f"{exe_dir}\\_internal\\query.py")
eel.init("web")

# 2. Fonctions d'authentification
@eel.expose
def get_data(nni, mdp)

# 3. Fonctions de récupération de données
@eel.expose
def get_gmr()
@eel.expose
def get_filters(gmr, date_start, date_end)

# 4. Fonctions d'interface utilisateur
@eel.expose
def get_og(), get_ni(), go_back()

# 5. Fonction de génération Excel
@eel.expose
def generate_excel(operation)

# 6. Point d'entrée principal
eel.start("./index.html", size=(315, 535), mode='default')
```

### Flux d'Exécution Principal
1. **Initialisation** : Configuration des chemins et démarrage du serveur Eel
2. **Authentification** : Validation credentials et stockage session
3. **Sélection GMR/Dates** : Interface de filtrage avec validation
4. **Traitement des opérations** : Récupération, filtrage et validation métier
5. **Sélection OG/NI** : Interface de choix avec recherche et sélection multiple
6. **Génération Excel** : Création automatisée de fiches de coordination

### Gestion d'État Global
```python
# Variables globales partagées
global headers      # Headers d'authentification API
global og          # Liste des Opérations Globales filtrées
global ni          # Liste des Notes d'Information filtrées
global main_gmr    # GMR sélectionné pour le contexte
```

### Algorithmes de Validation Métier
```python
# Validation complexe des opérations
for operation_globale in dic_operations_unique:
    query = query_get_equipes_intervenantes(dic_operations_unique[operation_globale][0]['NUMERO_NI'])
    list_equipe = make_query(query, headers)
    
    if is_operation_valid(dic_operations_unique[operation_globale], list_equipe):
        # Formatage avec statut coloré
        statut = dic_operations_unique[operation_globale][0]['STATUT_NI']
        color_map = {
            'Diffusée': 'blue',
            'Sans Objet': 'lightgray',
            'En construction': 'orange',
            'Validée': 'green'
        }
```

## Exemples d'Utilisation

### Lancement de l'Application
```python
# Démarrage du serveur avec interface web
python script.py

# Configuration automatique :
# - Taille fenêtre : 315x535 pixels
# - Mode par défaut : navigateur intégré
# - Point d'entrée : index.html
```

### Workflow Utilisateur Complet
```python
# 1. Authentification (appelée depuis index.html)
eel.get_data("123456", "motdepasse")
# → Validation credentials → Redirection vers filters.html

# 2. Récupération GMR (appelée depuis filters.html)
eel.get_gmr()
# → Retour liste GMR → Affichage interface de sélection

# 3. Application des filtres (depuis filters.html)
eel.get_filters("GMR_NORD", "2024-01-01", "2024-12-31")
# → Traitement + validation → Redirection vers OG_choice.html

# 4. Récupération des listes filtrées (depuis OG_choice.html)
eel.get_og()  # → Retour liste OG filtrées
eel.get_ni()  # → Retour liste NI filtrées

# 5. Génération Excel (depuis OG_choice.html)
eel.generate_excel("OG-2024-0001")
# → Création fiche Excel personnalisée
```

### Intégration avec Interface Web
```javascript
// Côté JavaScript - Communication bidirectionnelle
eel.get_data(nni, mdp);                    // Appel Python depuis JS
eel.display_error(response_tuple);         // Callback JS depuis Python
eel.go_to('./pages/filters.html');        // Navigation contrôlée

// Pattern d'exposition des fonctions
eel.expose(display_gmr);
function display_gmr(li_GMR) {
    // Traitement côté client des données serveur
}
```

## Configuration & Paramètres

### Configuration du Serveur Eel
```python
# Paramètres de fenêtre
WINDOW_SIZE = (315, 535)
WINDOW_MODE = 'default'
ENTRY_POINT = "./index.html"

# Répertoires de l'application
WEB_DIR = "web"                    # Interface utilisateur
INTERNAL_DIR = "_internal"         # Ressources internes
OUTPUT_DIR = "ficheExcel"         # Fichiers Excel générés
```

### Template et Ressources
```python
# Fichier template Excel
TEMPLATE_PATH = "./_internal/TEMPLATE.xlsm"
SHEET_NAME = 'FicheDeCoordination'

# Cellules de référence dans le template
TITLE_CELL = "A1"                 # Titre de la fiche
GMR_INFO_CELLS = ["S4", "I4", "C4", "AM4"]  # Informations en-tête
DATE_CELLS = ["D9", "K9", "D10", "K10"]     # Dates et semaines
CALENDAR_START = "AT7"            # Début du calendrier
```

### Mapping des Statuts d'Opération
```python
color_map = {
    'Diffusée': 'blue',
    'Sans Objet': 'lightgray',
    'En construction': 'orange',
    'Validée': 'green'
}
```

### Paramètres de Nomenclature des Fichiers
```python
# Format de nommage automatique
# FC_{NUMERO_NI}_S{semaine_debut}_S{semaine_fin}_{adresse}_V0.xlsm
file_name = f"ficheExcel/FC_{data_row['NUMERO_NI']}_S{start_date.strftime('%W')}_S{end_date.strftime('%W')}_{adr_filename}_V0.xlsm"

# Caractères interdits remplacés par '_'
FORBIDDEN_CHARS = '<>?[]:|/'
```

## Notes Techniques

### Optimisations de Performance
```python
# Mesure de temps d'exécution
start = time.time()
# ... traitement ...
end = time.time()
print(f"traitement de {len(og_ni)} en {end - start} secondes")

# Traitement en lots pour éviter les requêtes multiples
dic_operations_unique = {}
for i in range(len(og_ni)):
    if og_ni[i]["NUMERO_OG"] not in dic_operations_unique:
        dic_operations_unique[og_ni[i]["NUMERO_OG"]] = []
    dic_operations_unique[og_ni[i]["NUMERO_OG"]].append(og_ni[i])
```

### Gestion des Années Bissextiles
```python
# Calcul automatique pour les opérations à cheval sur années
if operation_end_day_number < operation_start_day_number:
    operation_end_day_number += days_in_year(int(start_date.strftime("%Y")))
```

### Robustesse et Gestion d'Erreurs
```python
# Validation des entrées avec valeurs par défaut
equipes_pilotes = make_query(query, headers) or []
equipes_intervenantes = make_query(query, headers) or []

# Gestion des caractères spéciaux dans les noms de fichiers
for char in '<>?[]:|/':
    adr_filename = adr_filename.replace(char, '_')

# Protection contre les index hors limites
if getColumn(j) == 'AM':  # Limite calendrier
    break
```

### Patterns d'Architecture
- **Global State Management** : Variables globales pour état d'application
- **Template Method** : Pattern de génération Excel avec template fixe
- **Bridge Pattern** : Eel comme pont entre Python et JavaScript
- **Strategy Pattern** : Différentes stratégies selon type d'opération (OG/NI)

### Limitations Connues
- **Excel requis** : Dépendance à Microsoft Excel via xlwings
- **Mono-utilisateur** : Variables globales partagées
- **Pas de cache** : Requêtes répétées vers la base de données

## Maintenance & Développement

### Extension des Fonctionnalités
```python
# Ajout d'une nouvelle fonction exposée
@eel.expose
def nouvelle_fonctionnalite(param1, param2):
    """
    Nouvelle fonctionnalité à documenter
    """
    # Logique métier
    result = process_data(param1, param2)
    return result

# Côté JavaScript correspondant
eel.expose(handle_nouvelle_fonctionnalite);
function handle_nouvelle_fonctionnalite(data) {
    // Traitement côté client
}
```

### Modification du Template Excel
```python
# Ajout de nouvelles cellules de référence
NEW_REFERENCE_CELLS = {
    'nouvelle_info': 'AZ1',
    'autre_donnee': 'BA2'
}

# Dans generate_excel()
sheet[NEW_REFERENCE_CELLS['nouvelle_info']].value = nouvelle_valeur
```

### Debugging et Monitoring
```python
# Ajout de logs détaillés
import logging

logging.basicConfig(level=logging.DEBUG)

@eel.expose
def get_filters(gmr, date_start, date_end):
    logging.info(f"Début traitement: GMR={gmr}, période={date_start} à {date_end}")
    start = time.time()
    
    # ... logique existante ...
    
    logging.info(f"Traitement terminé: {len(og)} OG, {len(ni)} NI en {end-start:.2f}s")
```

### Tests et Validation
```python
# Tests unitaires recommandés
def test_generate_excel():
    """Test de génération Excel avec données mockées"""
    mock_operation = "OG-TEST-001"
    # Mock des dépendances
    # Validation du fichier généré

def test_validation_operations():
    """Test des règles de validation métier"""
    valid_operation = create_mock_valid_operation()
    invalid_operation = create_mock_invalid_operation()
    
    assert is_operation_valid(valid_operation, mock_equipes) == True
    assert is_operation_valid(invalid_operation, mock_equipes) == False
```

### Guidelines de Contribution
1. **Documentation** : Commenter les fonctions exposées à Eel
2. **Gestion d'erreurs** : Toujours gérer les cas d'échec des requêtes
3. **Performance** : Mesurer les temps d'exécution pour les opérations longues
4. **Compatibilité** : Tester avec différentes versions d'Excel
5. **Sécurité** : Ne jamais exposer de credentials via Eel
6. **State Management** : Minimiser l'usage des variables globales

### Fichiers Associés à Modifier
- **[web/](../web/)** : Interface utilisateur et scripts JavaScript
- **[query.py](../query.py)** : Nouvelles requêtes SQL si nécessaire
- **[function_utils.py](../function_utils.py)** : Fonctions utilitaires métier
- **[TEMPLATE.xlsm](../TEMPLATE.xlsm)** : Template Excel à modifierS