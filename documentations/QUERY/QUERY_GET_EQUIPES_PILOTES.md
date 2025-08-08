# Analyse SQL - Fonction `query_get_equipes_pilotes()`

## Table des Matières
- [Résumé de la Requête](#résumé-de-la-requête)
- [Schéma Arborescent des Tables et Données](#schéma-arborescent-des-tables-et-données)
- [Mappage des Relations](#mappage-des-relations)
- [Dictionnaire des Données Extraites](#dictionnaire-des-données-extraites)
- [Analyse des Contraintes et Filtres](#analyse-des-contraintes-et-filtres)
- [Performance et Optimisations](#performance-et-optimisations)

## 1. Résumé de la Requête

```
Objectif : Extraction des codes d'équipes pilotes associées à un GMR spécifique
Type : SELECT simple avec jointure
Complexité : Simple
Tables impliquées : 2
```

**Code SQL :**
```sql
SELECT TB023_EQUIPE_RGPD.CODE 
FROM "PUBLIC".ANIS."TB023_EQUIPE_RGPD" 
LEFT JOIN "PUBLIC".ANIS."TB009_GMR" 
    ON TB009_GMR.ID_GMR = TB023_EQUIPE_RGPD.ID_GMR 
WHERE TB009_GMR.LIBELLE = '{gmr}'
```

## 2. Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
├── TB023_EQUIPE_RGPD (table principale)
│   ├── Colonnes sélectionnées :
│   │   └── CODE (VARCHAR) → Code d'équipe pilote
│   └── Conditions appliquées :
│       ├── WHERE : Filtrage indirect via jointure GMR
│
└── JOINTURES
    └── [LEFT JOIN] TB009_GMR
        ├── Relation : TB023_EQUIPE_RGPD.ID_GMR ↔ TB009_GMR.ID_GMR
        ├── Colonnes utilisées :
        │   ├── ID_GMR → Clé de jointure
        │   └── LIBELLE → Filtre de sélection
        └── Conditions : WHERE LIBELLE = '{gmr}'
```

## 3. Mappage des Relations

```
GRAPHE DES RELATIONS
TB023_EQUIPE_RGPD ────[ID_GMR]────► TB009_GMR
        │                              │
        │                              │
        └── CODE (OUTPUT)              └── LIBELLE (FILTER = '{gmr}')
```

## 4. Dictionnaire des Données Extraites

| Table | Colonne | Alias/Utilisation | Type Présumé | Rôle dans le Résultat |
|-------|---------|-------------------|--------------|----------------------|
| TB023_EQUIPE_RGPD | CODE | - | VARCHAR | Code identificateur équipe pilote |

## 5. Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
├── Filtres sur TB009_GMR
│   └── WHERE LIBELLE = '{gmr}' (filtre exact sur nom GMR)
│
└── Conditions de Jointure
    └── LEFT JOIN : TB023_EQUIPE_RGPD.ID_GMR = TB009_GMR.ID_GMR
        └── Préservation : Garde toutes les équipes même sans GMR associé
```

## 6. Performance et Optimisations Suggérées

### Points d'Attention
- **Requête simple** : Performance généralement excellente
- **Jointure LEFT** : Peut retourner des résultats même si GMR n'existe pas
- **Filtre exact** : Utilisation d'égalité stricte (plus performant que LIKE)
- **Pas de tri** : Ordre des résultats non déterministe

### Optimisations Possibles

1. **Amélioration de la jointure**
```sql
-- Remplacer LEFT JOIN par INNER JOIN si les équipes doivent avoir un GMR
SELECT TB023_EQUIPE_RGPD.CODE 
FROM "PUBLIC".ANIS."TB023_EQUIPE_RGPD" 
INNER JOIN "PUBLIC".ANIS."TB009_GMR" 
    ON TB009_GMR.ID_GMR = TB023_EQUIPE_RGPD.ID_GMR 
WHERE TB009_GMR.LIBELLE = '{gmr}'
```

2. **Ajout d'un tri pour la cohérence**
```sql
-- Ajouter ORDER BY pour un résultat déterministe
ORDER BY TB023_EQUIPE_RGPD.CODE
```

3. **Gestion des valeurs nulles**
```sql
-- Filtrer les codes d'équipe non vides
WHERE TB009_GMR.LIBELLE = '{gmr}' 
  AND TB023_EQUIPE_RGPD.CODE IS NOT NULL 
  AND TB023_EQUIPE_RGPD.CODE != ''
```

4. **Optimisation avec DISTINCT si nécessaire**
```sql
-- Éviter les doublons si une équipe peut être liée plusieurs fois
SELECT DISTINCT TB023_EQUIPE_RGPD.CODE 
FROM ...
```

### Métriques de Performance Attendues
- **Temps d'exécution** : < 100ms (requête très simple)
- **Lignes retournées** : 1-20 équipes pilotes par GMR (généralement)
- **Index utilisés** : 2-3 index pour performance optimale

### Cas d'Usage dans l'Application

#### Contexte d'Utilisation
```python
# Dans script.py - Fonction get_equipes_pilotes()
from query import query_get_equipes_pilotes
from query_utils import make_query

def get_equipes_pilotes(gmr, headers):
    query = query_get_equipes_pilotes(gmr)
    result = make_query(query, headers)
    equipes = [equipe['CODE'] for equipe in result]
    return equipes
```

#### Exemple de Résultat
```json
[
    {"CODE": "EQPIL001"},
    {"CODE": "EQPIL002"},
    {"CODE": "EQPIL003"}
]
```

#### Traitement Post-Requête
```python
# Transformation en liste simple
equipes_pilotes = [equipe['CODE'] for equipe in result]
# Résultat : ["EQPIL001", "EQPIL002", "EQPIL003"]
```

### Intégration avec d'Autres Requêtes
- **`query_to_get_gmr()`** : Fournit la liste des GMR disponibles pour le paramètre
- **`query_get_equipes_intervenantes()`** : Complément pour récupérer les équipes d'intervention
- **Applications métier** : Sélection d'équipes pour attribution d'opérations

### Notes de Maintenance

#### Évolutions Possibles
1. **Ajout de filtres** : Équipes actives uniquement, par type d'équipe

#### Surveillance Recommandée
- Vérifier que chaque GMR a au moins une équipe pilote
- Valider la cohérence des codes d'équipe retournés