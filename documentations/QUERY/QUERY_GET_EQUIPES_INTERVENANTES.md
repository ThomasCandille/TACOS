# Analyse SQL - Fonction `query_get_equipes_intervenantes()`

## Table des Matières
- [Résumé de la Requête](#résumé-de-la-requête)
- [Schéma Arborescent des Tables et Données](#schéma-arborescent-des-tables-et-données)
- [Mappage des Relations](#mappage-des-relations)
- [Dictionnaire des Données Extraites](#dictionnaire-des-données-extraites)
- [Analyse des Contraintes et Filtres](#analyse-des-contraintes-et-filtres)
- [Performance et Optimisations](#performance-et-optimisations)

## 1. Résumé de la Requête

```
Objectif : Extraction des codes d'équipes intervenantes pour une Note d'Information spécifique avec filtrage métier
Type : SELECT avec jointures multiples et filtres complexes
Complexité : Moyenne
Tables impliquées : 3
```

**Code SQL :**
```sql
SELECT CODE 
FROM "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TB017_PARTIE_PRENANTE_RGPD" 
LEFT JOIN "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TB020_NI_PP" 
    ON TB017_PARTIE_PRENANTE_RGPD.ID_PARTIE_PRENANTE = TB020_NI_PP.ID_PP 
LEFT JOIN "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TB001_NOTE_INFORMATION" 
    ON TB020_NI_PP.ID_NI = TB001_NOTE_INFORMATION.ID_NI 
WHERE NUMERO_NI = '{numero_ni}' 
  AND TYPE != 'Client' 
  AND NOM NOT LIKE '%COSE%'
```

## 2. Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
├── TB017_PARTIE_PRENANTE_RGPD (table principale)
│   ├── Colonnes sélectionnées :
│   │   └── CODE (VARCHAR) → Code équipe intervenante
│   └── Conditions appliquées :
│       ├── WHERE : Filtrage métier sur TYPE et NOM
│       └── Filtres : TYPE != 'Client' AND NOM NOT LIKE '%COSE%'
│
└── JOINTURES
    ├── [LEFT JOIN] TB020_NI_PP (table de liaison)
    │   ├── Relation : TB017_PARTIE_PRENANTE_RGPD.ID_PARTIE_PRENANTE ↔ TB020_NI_PP.ID_PP
    │   ├── Colonnes utilisées :
    │       ├── ID_PP → Clé de liaison vers partie prenante
    │       └── ID_NI → Clé de liaison vers note d'information
    │
    └── [LEFT JOIN] TB001_NOTE_INFORMATION
        ├── Relation : TB020_NI_PP.ID_NI ↔ TB001_NOTE_INFORMATION.ID_NI
        ├── Colonnes utilisées :
        │   └── NUMERO_NI → Filtre de sélection par numéro NI
        └── Conditions : WHERE NUMERO_NI = '{numero_ni}'
```

## 3. Mappage des Relations

```
GRAPHE DES RELATIONS
TB017_PARTIE_PRENANTE_RGPD ────[ID_PARTIE_PRENANTE = ID_PP]────► TB020_NI_PP ────[ID_NI]────► TB001_NOTE_INFORMATION
        │                                                               │                              │
        │                                                               │                              │
        ├── CODE (OUTPUT)                                               │                              │
        ├── TYPE (FILTER ≠ 'Client')                                    │                              │
        └── NOM (FILTER NOT LIKE '%COSE%')                              │                              └── NUMERO_NI (FILTER = '{numero_ni}')
                                                                        │
                                                                        └── (Table de liaison N:M)
```

## 4. Dictionnaire des Données Extraites

| Table | Colonne | Alias/Utilisation | Type Présumé | Rôle dans le Résultat |
|-------|---------|-------------------|--------------|----------------------|
| TB017_PARTIE_PRENANTE_RGPD | CODE | - | VARCHAR | Code identificateur équipe intervenante |

## 5. Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
├── Filtres sur TB001_NOTE_INFORMATION
│   └── WHERE NUMERO_NI = '{numero_ni}' (sélection de la NI spécifique)
│
├── Filtres sur TB017_PARTIE_PRENANTE_RGPD
│   ├── AND TYPE != 'Client' (exclusion des clients)
│   └── AND NOM NOT LIKE '%COSE%' (exclusion des entités COSE)
│
└── Conditions de Jointure
    ├── LEFT JOIN TB020_NI_PP : Liaison partie prenante ↔ note d'information
    └── LEFT JOIN TB001_NOTE_INFORMATION : Accès aux détails de la NI
```

## 6. Performance et Optimisations Suggérées

### Points d'Attention
- **Jointures en chaîne** : 3 tables liées par des clés étrangères
- **Filtres métier complexes** : TYPE et NOM avec conditions négatives
- **Cardinalité** : Relation N:M entre parties prenantes et NI
- **Performance** : LIKE avec wildcards des deux côtés peut être lent

### Optimisations Possibles

1. **Amélioration du filtre LIKE**
```sql
-- Si possible, remplacer par une liste d'exclusions exactes
WHERE NUMERO_NI = '{numero_ni}' 
  AND TYPE != 'Client' 
  AND NOM NOT IN ('COSE_ENTITY1', 'COSE_ENTITY2', ...)
```

2. **Ajout d'un tri pour la cohérence**
```sql
-- Ajouter ORDER BY pour un résultat déterministe
ORDER BY TB017_PARTIE_PRENANTE_RGPD.CODE
```

3. **Optimisation avec DISTINCT si nécessaire**
```sql
-- Éviter les doublons si une équipe peut être liée plusieurs fois
SELECT DISTINCT CODE 
FROM ...
```

4. **Filtre de validation des codes**
```sql
-- S'assurer que les codes ne sont pas vides
WHERE NUMERO_NI = '{numero_ni}' 
  AND TYPE != 'Client' 
  AND NOM NOT LIKE '%COSE%'
  AND CODE IS NOT NULL 
  AND CODE != ''
```

### Métriques de Performance Attendues
- **Lignes retournées** : 1-10 équipes intervenantes par NI (généralement)
- **Index utilisés** : 3-4 index pour performance optimale
- **Complexité** : O(n) où n = nombre de parties prenantes liées à la NI

### Cas d'Usage dans l'Application

#### Contexte d'Utilisation
```python
# Dans script.py - Fonction get_equipes_intervenantes()
from query import query_get_equipes_intervenantes
from query_utils import make_query

def get_equipes_intervenantes(numero_ni, headers):
    query = query_get_equipes_intervenantes(numero_ni)
    result = make_query(query, headers)
    equipes = [equipe['CODE'] for equipe in result]
    return equipes
```

#### Exemple de Résultat
```json
[
    {"CODE": "EQINT001"},
    {"CODE": "EQINT002"},
    {"CODE": "EQINT003"}
]
```

#### Traitement Post-Requête
```python
# Transformation en liste simple
equipes_intervenantes = [equipe['CODE'] for equipe in result]
# Résultat : ["EQINT001", "EQINT002", "EQINT003"]

# Validation des équipes récupérées
equipes_valides = [code for code in equipes_intervenantes if code and len(code) > 0]
```

### Logique Métier des Filtres

#### Exclusion des Clients
```
TYPE != 'Client'
└── Justification : Les clients ne sont pas des équipes intervenantes opérationnelles
```

#### Exclusion des Entités COSE
```
NOM NOT LIKE '%COSE%'
└── Justification : Filtrage d'entités spécifiques
```

### Intégration avec d'Autres Requêtes
- **`query_get_equipes_pilotes()`** : Complément pour récupérer les équipes pilotes par GMR
- **`query_to_get_og_ni()`** : Fournit les numéros NI pour lesquels récupérer les équipes
- **Applications métier** : Attribution de tâches aux équipes intervenantes

### Évolutions Possibles

#### Optimisations Techniques
1. **Cache applicatif** : Mise en cache des équipes par NI pour réduire les appels
2. **Requête batch** : Traitement en lot pour plusieurs NI simultanément
3. **Index composites** : Optimisation des index pour les filtres combinés

### Notes de Maintenance

#### Surveillance Recommandée
- Vérifier que chaque NI a au moins une équipe intervenante
- Valider l'efficacité des filtres d'exclusion
- Contrôler la cohérence des codes d'équipe retournés

#### Points de Vigilance
- **Évolution des filtres métier** : Les critères d'exclusion peuvent évoluer
- **Intégrité référentielle** : S'assurer de la cohérence des liaisons N:M
- **Performance** : Surveiller l'impact des filtres LIKE sur de gros volumes