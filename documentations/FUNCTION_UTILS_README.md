# Documentation - function_utils.py

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
**Technologie :** Python 3.x avec module datetime  
**Position :** Couche utilitaire dans l'architecture TACOS  
**Rôle :** Fournit des fonctions d'assistance pour la manipulation de données, la validation métier et la génération de fichiers Excel dans l'application TACOS

### Description
Le fichier [`function_utils.py`](function_utils.py) constitue une bibliothèque de fonctions utilitaires essentielles pour le traitement des opérations globales et la génération des fiches de coordination Excel. Il centralise la logique métier de validation, les calculs de dates, la gestion des couleurs Excel et les algorithmes de positionnement de colonnes.

## Fonctionnalités Principales

### Gestion des Couleurs Excel
- **Mapping des codes équipes** : Association codes → couleurs RGB pour l'interface Excel
- **Configuration visuelle** : Application conditionnelle des couleurs de fond selon les types d'équipes
- **Gestion des cellules de référence** : Activation automatique des indicateurs visuels

```python
def get_background_color(code, sheet):
    color_mapping = {
        "STAIA": ("AS7", (61, 112, 172)),
        "STGP": ("AS9", (249, 115, 133)),
        "STEL": ("AS10", (111, 118, 123)),
        "STECC": ("AS11", (184, 159, 211)),
        "STEPP": ("AS13", (221, 223, 224))
    }
```

### Calculs Temporels et Calendaires
- **Extraction de jour d'année** : Conversion date → numéro de jour (1-365/366)
- **Gestion des années bissextiles** : Calcul automatique du nombre de jours par année
- **Parsing de dates** : Traitement des formats de date de la base de données

```python
def get_operation_day_number(operation_date):
    operation_start = operation_date[slice(0, 10)].split("-")
    operation_start_datetime = datetime.datetime(int(operation_start[0]), int(operation_start[1]),int(operation_start[2]))
    operation_start_day_number = operation_start_datetime.strftime("%j")
    return operation_start_day_number
```

### Génération de Références Excel
- **Algorithme de colonnes** : Conversion index numérique → référence Excel (H, I, ..., AA, AB)
- **Gestion multi-caractères** : Support des colonnes au-delà de Z
- **Positionnement de calendrier** : Mapping des jours vers les colonnes Excel

```python
def getColumn(index):
    ascii_of_A = 65
    ascii_of_H = 72
    ascii_of_Z = 90
    ascii_value = ascii_of_H + index
    if ascii_value > ascii_of_Z:
        ascii_second_letter = (ascii_value%ascii_of_Z)-1
        return "A" + chr(ascii_of_A + ascii_second_letter)
    return chr(ascii_value)
```

### Validation Métier des Opérations
- **Filtrage des parties prenantes** : Exclusion des sociétés tierces
- **Validation multiplicité** : Vérification présence de plusieurs intervenants
- **Contrôle des équipes** : Validation de la diversité des codes équipes
- **Exclusion CDI** : Filtrage des opérations de type CDI

```python
def is_operation_valid(operation, list_equipe):
    list_nom, list_partie_prenante = get_element_of_operation(operation)
    isNotPartiePrenante = list_partie_prenante.count('Societe tierce') == 0
    isMoreThanOne = len(list_partie_prenante) > 1
    isNotAlone = get_occurence_of_element(list_equipe)
    isNotDI = True
    # Validation logique métier...
    return is_valid
```

## Dépendances & Imports

### Bibliothèques Standard Python
```python
import datetime  # Manipulation des dates et calculs temporels
```

### Intégration avec l'Écosystème TACOS
- **[script.py](script.py)** : Utilisation dans la génération Excel via xlwings
- **[query.py](query.py)** : Traitement des données issues des requêtes ANIS
- **Template Excel** : Application des couleurs et positionnement dans TEMPLATE.xlsm

### Dépendances Implicites
- **xlwings** : Manipulation des feuilles Excel (via script.py)
- **Base de données ANIS** : Structure des données opérationnelles
- **Format de dates** : Conformité avec les formats YYYY-MM-DD de la base

## Structure du Code

### Organisation Fonctionnelle
```python
# 1. Fonctions de gestion visuelle Excel
get_background_color(code, sheet)

# 2. Fonctions de calculs temporels
get_operation_day_number(operation_date)
days_in_year(year)

# 3. Fonctions de positionnement Excel
getColumn(index)

# 4. Fonctions de traitement de données
get_element_of_operation(operations)
get_occurence_of_element(list_equipe)

# 5. Fonctions de validation métier
is_operation_valid(operation, list_equipe)
isEquipeHere(row)
```

### Algorithmes Clés

#### Algorithme de Colonnes Excel
```python
# Conversion index → colonne (H=0, I=1, ..., AA=19, AB=20)
def getColumn(index):
    ascii_of_A = 65  # 'A'
    ascii_of_H = 72  # 'H' (point de départ)
    ascii_of_Z = 90  # 'Z'
    ascii_value = ascii_of_H + index
    
    if ascii_value > ascii_of_Z:
        # Gestion des colonnes à deux lettres (AA, AB, etc.)
        ascii_second_letter = (ascii_value % ascii_of_Z) - 1
        return "A" + chr(ascii_of_A + ascii_second_letter)
    
    return chr(ascii_value)
```

#### Validation Métier Complexe
```python
def is_operation_valid(operation, list_equipe):
    # 1. Extraction des données d'opération
    list_nom, list_partie_prenante = get_element_of_operation(operation)
    
    # 2. Critères de validation
    isNotPartiePrenante = list_partie_prenante.count('Societe tierce') == 0
    isMoreThanOne = len(list_partie_prenante) > 1
    isNotAlone = get_occurence_of_element(list_equipe)
    
    # 3. Validation spécifique CDI
    isNotDI = True
    for nom in list_nom:
        if nom and nom.find("CDI") != -1:
            isNotDI = False
    
    # 4. Combinaison logique finale
    return isNotPartiePrenante and isMoreThanOne and isNotAlone and isNotDI
```

## Exemples d'Utilisation

### Génération de Calendrier Excel
```python
# Dans script.py - Utilisation typique pour génération Excel
from function_utils import get_background_color, getColumn, get_operation_day_number

# Application des couleurs par équipe
for i, result_row in enumerate(result_rows):
    if result_row.get('CODE_TB17'):
        background_color = get_background_color(result_row.get('CODE_TB17'), sheet)
        
        # Positionnement dans le calendrier
        operation_start_day = int(get_operation_day_number(result_row['DATE_DEB_NI']))
        first_day_operation = operation_start_day - operation_global_start_day_number
        
        # Application sur les colonnes Excel
        for j in range(first_day_operation, last_day_operation):
            if getColumn(j) == 'AM':  # Limite de colonnes
                break
            sheet[f'{getColumn(j)}{index + i*2}'].color = background_color
```

### Validation des Opérations
```python
# Dans script.py - Filtrage des opérations valides
from function_utils import is_operation_valid

# Récupération des équipes intervenantes
query = query_get_equipes_intervenantes(operation['NUMERO_NI'])
list_equipe = make_query(query, headers)

# Validation métier
if is_operation_valid(operation_data, list_equipe):
    # Traitement de l'opération valide
    og.append(f"{operation_data[0]['NUMERO_OG']} {detail}")
    ni.append(f"{operation_data[0]['NUMERO_NI']} {detail}")
```

### Calculs de Dates
```python
from function_utils import days_in_year, get_operation_day_number

# Gestion des changements d'année
start_year = int(start_date.strftime("%Y"))
operation_end_day = int(get_operation_day_number(operation_date))

if operation_end_day < operation_start_day:
    operation_end_day += days_in_year(start_year)
```

## Configuration & Paramètres

### Mapping des Couleurs d'Équipes
```python
color_mapping = {
    "STAIA": ("AS7", (61, 112, 172)),    # Équipe STAIA - Bleu
    "STGP": ("AS9", (249, 115, 133)),    # Équipe STGP - Rose
    "STEL": ("AS10", (111, 118, 123)),   # Équipe STEL - Gris
    "STECC": ("AS11", (184, 159, 211)),  # Équipe STECC - Violet
    "STEPP": ("AS13", (221, 223, 224))   # Équipe STEPP - Gris clair
}
```

### Paramètres de Colonnes Excel
```python
ascii_of_A = 65    # Point de départ alphabet
ascii_of_H = 72    # Première colonne calendrier (H)
ascii_of_Z = 90    # Limite alphabet simple
```

### Critères de Validation Métier
```python
# Types à exclure
EXCLUDED_PARTIE_PRENANTE = 'Societe tierce'
EXCLUDED_OPERATION_TYPE = 'CDI'

# Seuils de validation
MIN_PARTIE_PRENANTE = 1      # Minimum d'intervenants
MIN_EQUIPE_DIVERSITY = 1     # Minimum de codes équipes différents
```

### Cellules de Référence Excel
```python
# Cellules d'activation des couleurs dans TEMPLATE.xlsm
REFERENCE_CELLS = {
    "STAIA": "AS7",
    "STGP": "AS9", 
    "STEL": "AS10",
    "STECC": "AS11",
    "STEPP": "AS13"
}
```

## Notes Techniques

### Considérations de Performance
- **Algorithme O(1)** : Conversion index → colonne en temps constant
- **Validation en circuit court** : Arrêt dès qu'un critère invalide est détecté
- **Gestion mémoire** : Fonctions sans état, pas d'accumulation de données

### Optimisations Appliquées
```python
# Circuit court dans is_operation_valid
if list_partie_prenante.count('Societe tierce') != 0:
    return False  # Arrêt immédiat si société tierce

# Utilisation de set() pour unicité des codes
unique_codes = set()
for element in list_equipe:
    unique_codes.add(element['CODE'])
return len(unique_codes) > 1
```

### Gestion des Cas Limites
- **Dates invalides** : Protection contre les formats malformés
- **Codes équipes manquants** : Validation de l'existence avant traitement
- **Années bissextiles** : Calcul automatique via datetime
- **Colonnes Excel limites** : Arrêt à la colonne AM (limite pratique)

### Patterns d'Architecture
- **Pure Functions** : Fonctions sans effets de bord
- **Single Responsibility** : Une responsabilité par fonction
- **Dependency Injection** : Paramètres injectés (sheet, operations, etc.)
- **Fail-Fast** : Validation immédiate avec retour booléen

## Maintenance & Développement

### Extension des Types d'Équipes
```python
# Ajout d'un nouveau type d'équipe
def get_background_color(code, sheet):
    color_mapping = {
        # Équipes existantes...
        "NOUVELLE_EQUIPE": ("AS15", (255, 128, 0))  # Orange
    }
```

### Modification des Critères de Validation
```python
def is_operation_valid(operation, list_equipe):
    # Ajout d'un nouveau critère
    isValidRegion = check_region_validity(operation)
    
    return (isNotPartiePrenante and isMoreThanOne and 
            isNotAlone and isNotDI and isValidRegion)
```

### Extension du Mapping de Colonnes
```python
def getColumn(index):
    # Support des colonnes à trois lettres (AAA, AAB, etc.)
    if index > 701:  # Limite actuelle AA-AZ
        # Implémentation colonnes triple
        pass
```

### Tests Unitaires Recommandés
```python
# Tests pour get_background_color
def test_get_background_color():
    assert get_background_color("STAIA", mock_sheet) == (61, 112, 172)
    assert get_background_color("UNKNOWN", mock_sheet) == (255, 255, 255)

# Tests pour getColumn
def test_getColumn():
    assert getColumn(0) == "H"
    assert getColumn(18) == "Z" 
    assert getColumn(19) == "AA"

# Tests pour validation métier
def test_is_operation_valid():
    valid_operation = create_valid_operation()
    invalid_operation = create_invalid_operation()
    assert is_operation_valid(valid_operation, mock_equipes) == True
    assert is_operation_valid(invalid_operation, mock_equipes) == False
```

### Debugging et Monitoring
```python
# Ajout de logs pour debugging
import logging

def get_background_color(code, sheet):
    logging.debug(f"Recherche couleur pour code: {code}")
    # ... logique existante
    logging.debug(f"Couleur trouvée: {color}")
    return color

def is_operation_valid(operation, list_equipe):
    logging.info(f"Validation opération: {len(operation)} éléments")
    # ... logique existante
    logging.info(f"Résultat validation: {is_valid}")
    return is_valid
```

### Guidelines de Contribution
1. **Pureté fonctionnelle** : Maintenir les fonctions sans état
2. **Validation d'entrée** : Vérifier les paramètres en début de fonction
3. **Documentation** : Commenter les règles métier complexes
4. **Performance** : Privilégier les algorithmes O(1) ou O(n) linéaires
5. **Compatibilité Excel** : Tester les références de colonnes générées
6. **Robustesse** : Gérer les cas d'erreur (données manquantes, formats invalides)

### Fichiers Associés à Modifier
- **[script.py](script.py)** : Utilisation principale des fonctions utilitaires
- **TEMPLATE.xlsm** : Définition des cellules de référence couleurs
- **Tests unitaires** : Création de test_function_utils.py
- **Documentation** : Mise à jour des spécifications métier