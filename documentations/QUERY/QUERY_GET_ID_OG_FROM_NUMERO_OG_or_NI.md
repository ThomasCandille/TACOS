# Analyse SQL - Fonctions de Conversion d'Identifiants

## Table des Matières
- [Vue d'Ensemble](#vue-densemble)
- [Fonction query_get_id_og_from_numero_og](#fonction-query_get_id_og_from_numero_og)
- [Fonction query_get_id_og_from_numero_ni](#fonction-query_get_id_og_from_numero_ni)
- [Comparaison des Fonctions](#comparaison-des-fonctions)
- [Performance et Optimisations](#performance-et-optimisations)

## Vue d'Ensemble

Ces deux fonctions constituent un ensemble de **convertisseurs d'identifiants** permettant de récupérer l'identifiant technique (`ID_OG`) d'une Opération Globale à partir de différents identifiants métier.

---

## Fonction `query_get_id_og_from_numero_og`

### 1. Résumé de la Requête
```
Objectif : Conversion du numéro métier OG vers l'identifiant technique ID_OG
Type : SELECT simple avec filtre
Complexité : Simple
Tables impliquées : 1
```

**Code SQL :**
```sql
SELECT ID_OG 
FROM "PUBLIC".ANIS."TB025_OPERATION_GLOBALE" 
WHERE NUMERO_OG = '{numero_og}'
```

### 2. Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
└── TB025_OPERATION_GLOBALE (table unique)
    ├── Colonnes sélectionnées :
    │   └── ID_OG (INTEGER) → Identifiant technique de l'OG
    └── Conditions appliquées :
        └── WHERE : NUMERO_OG = '{numero_og}' (filtre exact)
```

### 3. Mappage des Relations

```
GRAPHE DES RELATIONS
TB025_OPERATION_GLOBALE (Table isolée - aucune jointure)
        │
        ├── NUMERO_OG (INPUT) ──────► Filtre de recherche
        └── ID_OG (OUTPUT) ──────► Résultat technique
```

### 4. Dictionnaire des Données Extraites

| Table | Colonne | Alias/Utilisation | Type Présumé | Rôle dans le Résultat |
|-------|---------|-------------------|--------------|----------------------|
| TB025_OPERATION_GLOBALE | ID_OG | - | INTEGER | Identifiant technique OG |

### 5. Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
└── Filtres sur TB025_OPERATION_GLOBALE
    └── WHERE NUMERO_OG = '{numero_og}' (égalité stricte)
```

---

## Fonction `query_get_id_og_from_numero_ni`

### 1. Résumé de la Requête
```
Objectif : Conversion du numéro métier NI vers l'identifiant technique ID_OG parent
Type : SELECT simple avec filtre
Complexité : Simple
Tables impliquées : 1
```

**Code SQL :**
```sql
SELECT ID_OG 
FROM "PUBLIC".ANIS."TB001_NOTE_INFORMATION" 
WHERE NUMERO_NI = '{numero_ni}'
```

### 2. Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
└── TB001_NOTE_INFORMATION (table unique)
    ├── Colonnes sélectionnées :
    │   └── ID_OG (INTEGER) → Identifiant technique de l'OG parent
    └── Conditions appliquées :
        └── WHERE : NUMERO_NI = '{numero_ni}' (filtre exact)
```

### 3. Mappage des Relations

```
GRAPHE DES RELATIONS
TB001_NOTE_INFORMATION (Table isolée - aucune jointure)
        │
        ├── NUMERO_NI (INPUT) ──────► Filtre de recherche
        └── ID_OG (OUTPUT) ──────► Résultat technique (OG parent)
```

### 4. Dictionnaire des Données Extraites

| Table | Colonne | Alias/Utilisation | Type Présumé | Rôle dans le Résultat |
|-------|---------|-------------------|--------------|----------------------|
| TB001_NOTE_INFORMATION | ID_OG | - | INTEGER | Identifiant technique OG parent |

### 5. Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
└── Filtres sur TB001_NOTE_INFORMATION
    └── WHERE NUMERO_NI = '{numero_ni}' (égalité stricte)
```

---

## Comparaison des Fonctions

### Similitudes
- **Structure identique** : SELECT simple avec WHERE
- **Objectif commun** : Récupération d'ID_OG
- **Performance similaire** : Requêtes très rapides
- **Complexité** : Simple (1 table, 1 filtre)

### Différences Clés

| Aspect | query_get_id_og_from_numero_og | query_get_id_og_from_numero_ni |
|--------|-------------------------------|-------------------------------|
| **Table source** | TB025_OPERATION_GLOBALE | TB001_NOTE_INFORMATION |
| **Paramètre d'entrée** | NUMERO_OG (numéro OG) | NUMERO_NI (numéro NI) |
| **Relation** | Conversion directe OG→ID | Récupération OG parent via NI |
| **Cardinalité** | 1:1 (un OG = un ID) | N:1 (plusieurs NI → même OG) |

### Flux Logique

```
CONVERSION D'IDENTIFIANTS

Chemin 1: NUMERO_OG ──────► query_get_id_og_from_numero_og() ──────► ID_OG
                                        │
                                        ▼
                               TB025_OPERATION_GLOBALE

Chemin 2: NUMERO_NI ──────► query_get_id_og_from_numero_ni() ──────► ID_OG
                                        │
                                        ▼
                               TB001_NOTE_INFORMATION
                                        │
                                        └── (contient ID_OG parent)
```

## Performance et Optimisations

### Points d'Attention
- **Requêtes très simples** : Performance excellente attendue
- **Cardinalité** : Résultat unique ou vide pour chaque appel
- **Sécurité** : Utilisation de paramètres (protection contre injection SQL)
- **Cohérence** : Pas de validation d'existence des identifiants

### Optimisations Possibles

1. **Gestion des cas d'erreur**
```sql
-- Ajouter une validation d'existence
SELECT ID_OG 
FROM "PUBLIC".ANIS."TB025_OPERATION_GLOBALE" 
WHERE NUMERO_OG = '{numero_og}' 
  AND NUMERO_OG IS NOT NULL
```

2. **Cache applicatif**
```python
# Mise en cache des conversions fréquentes
conversion_cache = {}

def get_id_og_cached(numero_og, headers):
    if numero_og not in conversion_cache:
        query = query_get_id_og_from_numero_og(numero_og)
        result = make_query(query, headers)
        conversion_cache[numero_og] = result[0]['ID_OG'] if result else None
    return conversion_cache[numero_og]
```

3. **Validation des paramètres**
```python
def query_get_id_og_from_numero_og(numero_og):
    if not numero_og or numero_og.strip() == '':
        raise ValueError("NUMERO_OG ne peut pas être vide")
    return f"SELECT ID_OG FROM \"PRIV_ANIS\".INPUT.ANIS.\"PROD_ANIS\".ANIS.\"TB025_OPERATION_GLOBALE\" WHERE NUMERO_OG = '{numero_og}'"
```

### Métriques de Performance Attendues
- **Temps d'exécution** : < 50ms par requête
- **Lignes retournées** : 0 ou 1 ligne exactement
- **Index utilisés** : 1 index par fonction pour performance optimale
- **Utilisation mémoire** : Très faible (requêtes simples)

### Cas d'Usage dans l'Application

#### Contexte d'Utilisation
```python
# Conversion OG → ID technique
numero_og = "OG2024001"
id_og = get_id_from_numero_og(numero_og, headers)

# Conversion NI → ID technique de l'OG parent  
numero_ni = "NI2024001"
id_og_parent = get_id_from_numero_ni(numero_ni, headers)

# Utilisation pour requêtes complexes
operation_details = query_get_operation_intervention(id_og)
```

#### Intégration avec d'Autres Requêtes
- **`query_get_operation_intervention()`** : Utilise l'ID_OG comme paramètre
- **`query_to_get_og_ni()`** : Travaille avec les numéros métier
- **Scripts d'export** : Conversion pour traitement en lot

### Notes de Maintenance

#### Surveillance Recommandée
- Vérifier que tous les NUMERO_OG/NUMERO_NI recherchés existent
- Surveiller le temps de réponse (doit rester < 50ms)
- Contrôler l'intégrité référentielle ID_OG

#### Évolutions Possibles
1. **Validation métier** : Vérification des formats d'identifiants
2. **Batch processing** : Conversion en lot pour améliorer les performances