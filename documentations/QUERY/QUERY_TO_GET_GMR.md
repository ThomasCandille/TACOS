# Analyse SQL - Fonction `query_to_get_gmr()`

## Table des Matières
- [Résumé de la Requête](#résumé-de-la-requête)
- [Schéma Arborescent des Tables et Données](#schéma-arborescent-des-tables-et-données)
- [Mappage des Relations](#mappage-des-relations)
- [Dictionnaire des Données Extraites](#dictionnaire-des-données-extraites)
- [Analyse des Contraintes et Filtres](#analyse-des-contraintes-et-filtres)
- [Performance et Optimisations](#performance-et-optimisations)
- [Contexte d'Utilisation](#contexte-dutilisation)
- [Base de Données Cible](#base-de-données-cible)

## Résumé de la Requête

```
Objectif : Récupération de la liste distincte des libellés GMR
Type : SELECT avec DISTINCT
Complexité : Simple
Tables impliquées : 1
```

**Code SQL :**
```sql
SELECT DISTINCT TB009_GMR.LIBELLE AS GMR 
FROM "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TB009_GMR"
```

## Schéma Arborescent des Tables et Données

```
REQUÊTE PRINCIPALE
└── TB009_GMR
    ├── Colonnes sélectionnées :
    │   └── LIBELLE (VARCHAR) → GMR (alias pour affichage)
    └── Conditions appliquées :
        └── Filtres : DISTINCT (suppression des doublons)
```

## Mappage des Relations

```
GRAPHE DES RELATIONS
TB009_GMR (Table isolée - aucune jointure)
```

## Dictionnaire des Données Extraites

| Table | Colonne | Alias/Utilisation | Type Présumé | Rôle dans le Résultat |
|-------|---------|-------------------|--------------|----------------------|
| TB009_GMR | LIBELLE | GMR | VARCHAR | Nom/Description du groupe de maintenance |

## Analyse des Contraintes et Filtres

```
CONDITIONS APPLIQUÉES
└── Filtres sur TB009_GMR
    └── DISTINCT : Élimination des doublons sur LIBELLE
```

## Performance et Optimisations

### Index Recommandés
- **TB009_GMR.LIBELLE** : Index sur la colonne LIBELLE pour optimiser le DISTINCT

### Points d'Attention
- Requête simple avec performance généralement excellente
- Table de référence généralement de petite taille

### Optimisations Possibles
- Ajout d'un `ORDER BY LIBELLE` si un tri spécifique est souhaité
- Considérer un cache applicatif si cette liste change peu fréquemment
- Possibilité d'ajouter un filtre `WHERE LIBELLE IS NOT NULL` pour éviter les valeurs nulles

```sql
-- Version optimisée suggérée
SELECT DISTINCT TB009_GMR.LIBELLE AS GMR 
FROM "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TB009_GMR"
WHERE TB009_GMR.LIBELLE IS NOT NULL
ORDER BY TB009_GMR.LIBELLE
```

## Contexte d'Utilisation

### Rôle dans l'Architecture TACOS
Cette requête fait partie du système de gestion d'interventions ANIS et sert à :

- **Alimentation d'interfaces** : Remplir les listes déroulantes de GMR disponibles
- **Filtre de recherche** : Permettre la sélection d'un groupe de maintenance pour filtrer d'autres requêtes
- **Référentiel métier** : Fournir la liste des groupes de maintenance actifs

### Utilisation dans l'Application
```python
# Dans script.py - Fonction get_gmr()
from query import query_to_get_gmr
from query_utils import make_query

def get_gmr():
    query = query_to_get_gmr()
    result = make_query(query, headers)
    li_gmr = [gmr['GMR'] for gmr in result]
    return li_gmr
```

### Interactions avec d'Autres Requêtes
- **`query_to_get_og_ni()`** : Utilise le GMR sélectionné comme paramètre de filtrage
- **`query_get_equipes_pilotes()`** : Recherche les équipes pilotes d'un GMR spécifique

## Base de Données Cible

### Environnement de Production
```
Environnement : Production ANIS
Chemin complet : "PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TB009_GMR"
Schema : ANIS
Table : TB009_GMR (Table de référence des Groupes de Maintenance Réseau)
```

### Alternatives d'Environnement
```sql
-- Base de données intégration (disponible mais non utilisée)
"PUBLIC".ANIS."REC_ANIS".ANIS."TB009_GMR"

-- Base de données publique (alternative)
"PUBLIC".ANIS."TB009_GMR"
```

## Exemple de Résultat

### Sortie Attendue
```json
[
    {"GMR": "GMR NORD"},
    {"GMR": "GMR SUD"},
    {"GMR": "GMR EST"},
    {"GMR": "GMR OUEST"},
    {"GMR": "GMR CENTRE"}
]
```

### Traitement Post-Requête
```python
# Transformation en liste simple pour l'interface
li_gmr = [gmr['GMR'] for gmr in result]
# Résultat : ["GMR NORD", "GMR SUD", "GMR EST", "GMR OUEST", "GMR CENTRE"]
```

## Notes de Maintenance

### Évolutions Possibles
1. **Filtrage actif** : Ajouter une condition pour ne récupérer que les GMR actifs
2. **Tri personnalisé** : Implémenter un ordre de tri métier spécifique
3. **Cache** : Mettre en place un système de cache pour cette donnée référentielle stable

### Surveillance Recommandée
- Vérifier périodiquement que la table TB009_GMR contient des données
- Valider que tous les GMR retournés sont valides et utilisables