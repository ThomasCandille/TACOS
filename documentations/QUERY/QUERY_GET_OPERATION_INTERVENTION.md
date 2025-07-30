# Analyse SQL - Fonction `query_get_operation_intervention()`

## Table des Matières
- [Résumé de la Requête](#résumé-de-la-requête)
- [Schéma Arborescent des Tables et Données](#schéma-arborescent-des-tables-et-données)
- [Mappage des Relations](#mappage-des-relations)
- [Dictionnaire des Données Extraites](#dictionnaire-des-données-extraites)
- [Analyse des Contraintes et Filtres](#analyse-des-contraintes-et-filtres)
- [Performance et Optimisations](#performance-et-optimisations)

## 1. Résumé de la Requête

```
Objectif : Extraction complète des données d'intervention pour une opération globale spécifique
Type : SELECT complexe avec sous-requête d'agrégation
Complexité : Très Complexe
Tables impliquées : 11 (requête principale) + tables dans sous-requête
```

## 2. Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
├── TB001_NOTE_INFORMATION (table principale)
│   ├── Colonnes sélectionnées :
│   │   ├── NUMERO_NI (VARCHAR) → Identifiant métier NI
│   │   ├── DATE_DEB_NI (DATE) → Date début intervention
│   │   └── DATE_FIN_NI (DATE) → Date fin intervention
│   └── Conditions appliquées :
│       └── WHERE : Filtrage par ID_OG via jointures
│
├── JOINTURES
│   ├── [LEFT JOIN] TB002_INDICE
│   │   ├── Relation : TB001_NOTE_INFORMATION.ID_NI ↔ TB002_INDICE.ID_NI
│   │   ├── Colonnes utilisées :
│   │   │   └── NUMERO_INDICE → Numéro de version/indice
│   │   └── Conditions : Filtre sur MAX(NUMERO_INDICE) via sous-requête
│   │
│   ├── [LEFT JOIN] TB005_NI_OU
│   │   ├── Relation : TB001_NOTE_INFORMATION.ID_NI ↔ TB005_NI_OU.ID_NI
│   │   ├── Colonnes utilisées : ID_NI, ID_OU (liaison)
│   │
│   ├── [LEFT JOIN] TB004_OPERATION_UNITAIRE
│   │   ├── Relation : TB005_NI_OU.ID_OU ↔ TB004_OPERATION_UNITAIRE.ID_OU
│   │   ├── Colonnes utilisées :
│   │   │   ├── ID_OU → Identifiant technique OU
│   │   │   ├── LIBELLE_OU → Description opération unitaire
│   │   │   ├── NUMERO_OU → Numéro métier OU
│   │   │   └── ID_OUVRAGE → Clé vers ouvrage
│   │   └── Conditions : WHERE ID_OG = '{operation}'
│   │
│   ├── [LEFT JOIN] TB007_OUVRAGE
│   │   ├── Relation : TB004_OPERATION_UNITAIRE.ID_OUVRAGE ↔ TB007_OUVRAGE.ID_OUVRAGE
│   │   └── Colonnes utilisées :
│   │       ├── IDR → Identifiant réseau ouvrage
│   │       └── ADR → Adresse ouvrage
│   │
│   ├── [LEFT JOIN] TB015_OUVRAGE_GDP
│   │   ├── Relation : TB004_OPERATION_UNITAIRE.ID_OUVRAGE ↔ TB015_OUVRAGE_GDP.ID_OUVRAGE
│   │   └── Colonnes utilisées : ID_OUVRAGE, ID_GDP (liaison)
│   │
│   ├── [LEFT JOIN] TB014_GDP
│   │   ├── Relation : TB015_OUVRAGE_GDP.ID_GDP ↔ TB014_GDP.ID_GDP
│   │   └── Colonnes utilisées :
│   │       ├── CODE → Code GDP (alias CODE_TB14)
│   │       └── ID_GMR → Clé vers GMR
│   │
│   ├── [LEFT JOIN] TB009_GMR
│   │   ├── Relation : TB014_GDP.ID_GMR ↔ TB009_GMR.ID_GMR
│   │   └── Colonnes utilisées :
│   │       ├── LIBELLE → Nom GMR (alias GMR)
│   │       └── ID_GMR → Identifiant technique GMR
│   │
│   ├── [LEFT JOIN] TB018_OU_PP
│   │   ├── Relation : TB005_NI_OU.ID_OU ↔ TB018_OU_PP.ID_OU
│   │   └── Colonnes utilisées :
│   │       └── ID_OU → Identifiant OU (doublon avec TB004)
│   │
│   ├── [LEFT JOIN] TB017_PARTIE_PRENANTE_RGPD
│   │   ├── Relation : TB018_OU_PP.ID_PP ↔ TB017_PARTIE_PRENANTE_RGPD.ID_PARTIE_PRENANTE
│   │   └── Colonnes utilisées :
│   │       ├── NOM → Nom partie prenante
│   │       └── CODE → Code partie prenante (alias CODE_TB17)
│   │
│   └── [LEFT JOIN] TB025_OPERATION_GLOBALE
│       ├── Relation : TB001_NOTE_INFORMATION.ID_OG ↔ TB025_OPERATION_GLOBALE.ID_OG
│       └── Colonnes utilisées :
│           └── NUMERO_OG → Numéro opération globale
│
└── SOUS-REQUÊTES
    └── SOUS_REQUÊTE_1 (Sélection du dernier indice)
        ├── Tables : TB001_NOTE_INFORMATION, TB002_INDICE, TB005_NI_OU, TB004_OPERATION_UNITAIRE
        ├── Colonnes : MAX(NUMERO_INDICE)
        ├── Conditions : TB004_OPERATION_UNITAIRE.ID_OG = '{operation}'
        └── Utilisation : Garantir la récupération de la version la plus récente
```

## 3. Mappage des Relations

```
GRAPHE DES RELATIONS

TB001_NOTE_INFORMATION ────[ID_NI]────► TB002_INDICE
        │                                    │
        │                                    │ (sous-requête MAX)
        │                                    ▼
        │                              NUMERO_INDICE (filtre)
        │
        └─[ID_NI]────► TB005_NI_OU ────[ID_OU]────► TB004_OPERATION_UNITAIRE
        │                    │                              │
        │                    │                              │
        │                    └─[ID_OU]────► TB018_OU_PP     │
        │                              │                    │
        │                              │                    │
        │                    [ID_PP]───┘                    │
        │                              │                    │
        │                              ▼                    │
        │                    TB017_PARTIE_PRENANTE_RGPD     │
        │                                                   │
        └─[ID_OG]────► TB025_OPERATION_GLOBALE              │
                                                            │
                                               [ID_OUVRAGE]─┘
                                                            │
                                                            ▼
                                                    TB007_OUVRAGE
                                                            │
                                                            │
                                                    TB015_OUVRAGE_GDP
                                                            │
                                                [ID_GDP]────┘
                                                            │
                                                            ▼
                                                    TB014_GDP
                                                            │
                                                [ID_GMR]────┘
                                                            │
                                                            ▼
                                                    TB009_GMR
```

## 4. Dictionnaire des Données Extraites

| Table | Colonne | Alias/Utilisation | Type Présumé | Rôle dans le Résultat |
|-------|---------|-------------------|--------------|----------------------|
| TB004_OPERATION_UNITAIRE | ID_OU | - | INTEGER | Identifiant technique OU |
| TB018_OU_PP | ID_OU | - | INTEGER | Identifiant OU (redondant) |
| TB025_OPERATION_GLOBALE | NUMERO_OG | - | VARCHAR | Numéro opération globale |
| TB001_NOTE_INFORMATION | NUMERO_NI | - | VARCHAR | Numéro note information |
| TB001_NOTE_INFORMATION | DATE_DEB_NI | - | DATE | Date début intervention |
| TB001_NOTE_INFORMATION | DATE_FIN_NI | - | DATE | Date fin intervention |
| TB002_INDICE | NUMERO_INDICE | - | INTEGER | Version/indice document |
| TB004_OPERATION_UNITAIRE | LIBELLE_OU | - | VARCHAR | Description opération |
| TB004_OPERATION_UNITAIRE | NUMERO_OU | - | VARCHAR | Numéro opération unitaire |
| TB007_OUVRAGE | IDR | - | VARCHAR | Identifiant réseau |
| TB007_OUVRAGE | ADR | - | VARCHAR | Adresse ouvrage |
| TB014_GDP | CODE | CODE_TB14 | VARCHAR | Code GDP |
| TB017_PARTIE_PRENANTE_RGPD | NOM | - | VARCHAR | Nom intervenant |
| TB017_PARTIE_PRENANTE_RGPD | CODE | CODE_TB17 | VARCHAR | Code intervenant |
| TB009_GMR | LIBELLE | GMR | VARCHAR | Nom GMR |
| TB009_GMR | ID_GMR | - | INTEGER | Identifiant technique GMR |

## 5. Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
├── Filtres sur TB004_OPERATION_UNITAIRE
│   └── WHERE ID_OG = '{operation}' (filtre principal)
│
├── Conditions de Jointure
│   └── LEFT JOIN : Toutes les jointures préservent les données principales
│
└── Filtres d'Agrégation (Sous-requête)
    ├── SOUS_REQUÊTE_1 :
    │   ├── MAX(NUMERO_INDICE) : Récupération du dernier indice
    │   └── WHERE ID_OG = '{operation}' : Même filtre que requête principale
    │
    └── Filtre de Cohérence :
        └── AND TB002_INDICE.NUMERO_INDICE IN (sous-requête)
            └── But : Garantir la récupération de la version la plus récente
```

## 6. Performance et Optimisations Suggérées

### Points d'Attention
- **Redondance** : TB004_OPERATION_UNITAIRE.ID_OU et TB018_OU_PP.ID_OU (même information)
- **Sous-requête complexe** : MAX(NUMERO_INDICE) avec jointures multiples
- **Jointures en chaîne** : 11 tables jointes peuvent impacter les performances
- **Pas de tri** : Résultat non déterministe sans ORDER BY

### Optimisations Possibles

1. **Élimination de la redondance**
```sql
-- Supprimer TB018_OU_PP.ID_OU du SELECT (déjà présent via TB004)
SELECT TB004_OPERATION_UNITAIRE.ID_OU, /* TB018_OU_PP.ID_OU, */ ...
```

2. **Optimisation de la sous-requête**
```sql
-- Utiliser une CTE pour éviter la répétition de jointures
WITH max_indices AS (
    SELECT ID_NI, MAX(NUMERO_INDICE) as max_indice
    FROM TB002_INDICE i
    JOIN TB001_NOTE_INFORMATION ni ON i.ID_NI = ni.ID_NI
    JOIN TB005_NI_OU nou ON ni.ID_NI = nou.ID_NI
    JOIN TB004_OPERATION_UNITAIRE ou ON nou.ID_OU = ou.ID_OU
    WHERE ou.ID_OG = '{operation}'
    GROUP BY ID_NI
)
```

3. **Ajout d'un tri pour la cohérence**
```sql
-- Ajouter un ORDER BY pour un résultat déterministe
ORDER BY TB004_OPERATION_UNITAIRE.NUMERO_OU, TB001_NOTE_INFORMATION.NUMERO_NI
```

4. **Filtre de sécurité sur les indices**
```sql
-- Vérifier que l'indice existe
AND TB002_INDICE.NUMERO_INDICE IS NOT NULL
```

### Métriques de Performance Attendues
- **Lignes retournées** : Variable selon le nombre d'OU dans l'OG
- **Complexité** : O(n*m) où n = nombre d'OU et m = nombre d'indices

### Cas d'Usage Recommandés
- **Export Excel** : Génération de rapports détaillés d'intervention
- **Consultation métier** : Vue complète d'une opération globale
- **Traçabilité** : Suivi des versions et intervenants
