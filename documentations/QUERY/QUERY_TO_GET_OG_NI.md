# Analyse SQL - Fonction `query_to_get_og_ni()`

## Table des Matières
- [Résumé de la Requête](#résumé-de-la-requête)
- [Schéma Arborescent des Tables et Données](#schéma-arborescent-des-tables-et-données)
- [Mappage des Relations](#mappage-des-relations)
- [Dictionnaire des Données Extraites](#dictionnaire-des-données-extraites)
- [Analyse des Contraintes et Filtres](#analyse-des-contraintes-et-filtres)
- [Performance et Optimisations](#performance-et-optimisations)

## 1. Résumé de la Requête

```
Objectif : Extraction des Opérations Globales et Notes d'Information avec filtrage temporel et par GMR
Type : SELECT complexe avec sous-requêtes multiples
Complexité : Très Complexe
Tables impliquées : 10 (requête principale) + tables dans sous-requêtes
```

## 2. Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
├── TB001_NOTE_INFORMATION (table principale)
│   ├── Colonnes sélectionnées :
│   │   ├── NUMERO_NI (VARCHAR) → Identifiant métier NI
│   │   ├── STATUT_NI (VARCHAR) → Statut de la note d'information
│   │   ├── DATE_DEB_NI (DATE) → Date début (filtre temporel)
│   │   └── DATE_FIN_NI (DATE) → Date fin (filtre temporel)
│   └── Conditions appliquées :
│       └── WHERE : Filtrage temporel avec chevauchement de périodes
│
├── JOINTURES
│   ├── [LEFT JOIN] TB005_NI_OU
│   │   ├── Relation : TB001_NOTE_INFORMATION.ID_NI ↔ TB005_NI_OU.ID_NI
│   │   └── Colonnes utilisées : ID_NI, ID_OU (liaison)
│   │
│   ├── [LEFT JOIN] TB004_OPERATION_UNITAIRE
│   │   ├── Relation : TB005_NI_OU.ID_OU ↔ TB004_OPERATION_UNITAIRE.ID_OU
│   │   └── Colonnes utilisées : ID_OU, ID_OUVRAGE (liaison)
│   │
│   ├── [LEFT JOIN] TB007_OUVRAGE
│   │   ├── Relation : TB004_OPERATION_UNITAIRE.ID_OUVRAGE ↔ TB007_OUVRAGE.ID_OUVRAGE
│   │   └── Colonnes utilisées : ID_OUVRAGE (liaison)
│   │
│   ├── [LEFT JOIN] TB015_OUVRAGE_GDP
│   │   ├── Relation : TB004_OPERATION_UNITAIRE.ID_OUVRAGE ↔ TB015_OUVRAGE_GDP.ID_OUVRAGE
│   │   └── Colonnes utilisées : ID_OUVRAGE, ID_GDP (liaison)
│   │
│   ├── [LEFT JOIN] TB014_GDP
│   │   ├── Relation : TB015_OUVRAGE_GDP.ID_GDP ↔ TB014_GDP.ID_GDP
│   │   └── Colonnes utilisées : ID_GDP, ID_GMR (liaison)
│   │
│   ├── [LEFT JOIN] TB009_GMR
│   │   ├── Relation : TB014_GDP.ID_GMR ↔ TB009_GMR.ID_GMR
│   │   └── Colonnes utilisées :
│   │       ├── ID_GMR → Identifiant GMR
│   │       └── LIBELLE → Libellé GMR
│   │
│   ├── [LEFT JOIN] TB020_NI_PP
│   │   ├── Relation : TB005_NI_OU.ID_NI ↔ TB020_NI_PP.ID_NI
│   │   └── Colonnes utilisées : ID_NI, ID_PP (liaison)
│   │
│   ├── [LEFT JOIN] TB017_PARTIE_PRENANTE_RGPD
│   │   ├── Relation : TB020_NI_PP.ID_PP ↔ TB017_PARTIE_PRENANTE_RGPD.ID_PARTIE_PRENANTE
│   │   └── Colonnes utilisées :
│   │       ├── TYPE → Type de partie prenante
│   │       ├── CODE → Code partie prenante
│   │       └── NOM → Nom partie prenante
│   │
│   └── [LEFT JOIN] TB025_OPERATION_GLOBALE
│       ├── Relation : TB001_NOTE_INFORMATION.ID_OG ↔ TB025_OPERATION_GLOBALE.ID_OG
│       └── Colonnes utilisées :
│           └── NUMERO_OG → Numéro opération globale
│
├── SOUS-REQUÊTES
│   ├── SOUS_REQUÊTE_1 (Filtrage opérations avec >1 OU)
│   │   ├── Tables : TB001_NOTE_INFORMATION, TB025_OPERATION_GLOBALE, TB005_NI_OU, TB004_OPERATION_UNITAIRE
│   │   ├── Colonnes : NUMERO_OG
│   │   ├── Conditions : GROUP BY NUMERO_OG HAVING COUNT(ALL NUMERO_OG) > 1
│   │   └── Utilisation : Exclusion des opérations isolées
│   │
│   └── SOUS_REQUÊTE_2 (Filtrage par GMR)
│       ├── Tables : TB001_NOTE_INFORMATION, TB005_NI_OU, TB004_OPERATION_UNITAIRE, 
│       │            TB015_OUVRAGE_GDP, TB014_GDP, TB009_GMR, TB025_OPERATION_GLOBALE
│       ├── Colonnes : NUMERO_OG (DISTINCT)
│       ├── Conditions : TB009_GMR.LIBELLE LIKE '%{gmr}%'
│       └── Utilisation : Filtrage par GMR spécifique
│
└── AGRÉGATIONS & TRI
    └── ORDER BY : NUMERO_OG DESC
```

## 3. Mappage des Relations

```
GRAPHE DES RELATIONS

TB001_NOTE_INFORMATION ────[ID_NI]────► TB005_NI_OU ────[ID_OU]────► TB004_OPERATION_UNITAIRE
        │                                       │                               │
        │                                       │                               │
        └─[ID_OG]────► TB025_OPERATION_GLOBALE  │                               │
                                                │                               │
                                                └─[ID_NI]────► TB020_NI_PP      │
                                                                    │           │
                                                                    │           │
                                                        [ID_PP]────►│           │
                                                                    │           │
                                                TB017_PARTIE_PRENANTE_RGPD      │
                                                                                │
                                                                                │
                                                                [ID_OUVRAGE]────┘
                                                                                │
                                                                                ▼
                                                                    TB007_OUVRAGE
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
| TB025_OPERATION_GLOBALE | NUMERO_OG | - | VARCHAR | Identifiant métier principal |
| TB001_NOTE_INFORMATION | NUMERO_NI | - | VARCHAR | Identifiant note information |
| TB017_PARTIE_PRENANTE_RGPD | TYPE | - | VARCHAR | Type d'intervenant |
| TB009_GMR | ID_GMR | - | INTEGER | ID technique GMR |
| TB009_GMR | LIBELLE | - | VARCHAR | Nom du GMR |
| TB017_PARTIE_PRENANTE_RGPD | CODE | - | VARCHAR | Code partie prenante |
| TB017_PARTIE_PRENANTE_RGPD | NOM | - | VARCHAR | Nom partie prenante |
| TB001_NOTE_INFORMATION | STATUT_NI | - | VARCHAR | Statut de la NI |

## 5. Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
├── Filtres sur TB001_NOTE_INFORMATION
│   └── WHERE NOT (DATE_DEB_NI > TO_DATE('{date_end}','YYYY-MM-DD') 
│                 OR DATE_FIN_NI < TO_DATE('{date_start}','YYYY-MM-DD'))
│       └── Logique : Sélection des NI avec chevauchement de période
│
├── Conditions de Jointure
│   ├── LEFT JOIN : Toutes les jointures sont de type LEFT
│   └── Préservation : Garde toutes les NI même sans parties prenantes
│
├── Filtres d'Agrégation (Sous-requêtes)
│   ├── SOUS_REQUÊTE_1 :
│   │   ├── GROUP BY : NUMERO_OG
│   │   └── HAVING : COUNT(ALL NUMERO_OG) > 1
│   │       └── But : Exclure les opérations avec une seule OU
│   │
│   └── SOUS_REQUÊTE_2 :
│       ├── DISTINCT : NUMERO_OG (éviter doublons)
│       └── WHERE : TB009_GMR.LIBELLE LIKE '%{gmr}%'
│           └── But : Filtrer par GMR spécifique
│
└── Tri Final
    └── ORDER BY : NUMERO_OG DESC (plus récent en premier)
```

## 6. Performance et Optimisations Suggérées

### Points d'Attention
- **Requête très complexe** : 10 tables jointes + 2 sous-requêtes
- **Sous-requêtes coûteuses** : Répétition de jointures similaires
- **Filtrage temporel** : Logique NOT avec OR peut être lente
- **LIKE '%{gmr}%'** : Pattern matching sans index leading

### Optimisations Possibles

1. **Refactorisation des sous-requêtes**
```sql
-- Utiliser des CTE (Common Table Expressions) pour éviter répétition
WITH og_multi_ou AS (
    SELECT NUMERO_OG 
    FROM ... 
    GROUP BY NUMERO_OG 
    HAVING COUNT(*) > 1
),
og_by_gmr AS (
    SELECT DISTINCT NUMERO_OG 
    FROM ... 
    WHERE TB009_GMR.LIBELLE LIKE '%{gmr}%'
)
SELECT ... FROM ... WHERE NUMERO_OG IN (SELECT NUMERO_OG FROM og_multi_ou)
                      AND NUMERO_OG IN (SELECT NUMERO_OG FROM og_by_gmr)
```

2. **Optimisation du filtrage temporel**
```sql
-- Remplacer NOT (A OR B) par (NOT A AND NOT B)
WHERE TB001_NOTE_INFORMATION.DATE_DEB_NI <= TO_DATE('{date_end}','YYYY-MM-DD')
  AND TB001_NOTE_INFORMATION.DATE_FIN_NI >= TO_DATE('{date_start}','YYYY-MM-DD')
```

3. **Amélioration du filtrage GMR**
```sql
-- Si possible, utiliser égalité exacte au lieu de LIKE
WHERE TB009_GMR.LIBELLE = '{gmr}'
-- Ou optimiser le LIKE
WHERE TB009_GMR.LIBELLE LIKE '{gmr}%'  -- Plus efficace que '%{gmr}%'
```