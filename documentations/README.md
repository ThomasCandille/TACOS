# Documentation TACOS

## Aperçu du Dossier

Le dossier `documentations/` constitue le centre de documentation technique complet de l'application TACOS (Générateur de Fiches de Coordination). Il contient l'ensemble des spécifications détaillées, guides d'utilisation et documentations de maintenance pour tous les composants du projet.

**Objectif principal :** Fournir une documentation exhaustive et structurée permettant aux développeurs, mainteneurs et utilisateurs de comprendre, utiliser et étendre l'application TACOS de manière efficace.

## Structure du Dossier

```
documentations/
├── README.md                    # Documentation principale (ce fichier)
├── FUNCTION_UTILS_README.md     # Documentation du module function_utils.py
├── QUERY_README.md              # Documentation du module query.py
├── QUERY_UTILS_README.md        # Documentation du module query_utils.py
├── SCRIPT_README.md             # Documentation du script principal (script.py)
└── WEB/                         # Documentation des composants web
    ├── INDEX_README.md          # Documentation de la page d'accueil
    ├── CSS/
    │   └── STYLE_README.md      # Documentation de la feuille de style
    ├── JS/
    │   ├── EXCEL_README.md      # Documentation du module Excel JavaScript
    │   ├── FILTERS_README.md    # Documentation du module filtres JavaScript
    │   └── SCRIPT_README.md     # Documentation du script de connexion JavaScript
    └── PAGES/
        ├── FILTERS_README.md    # Documentation de la page de filtres
        └── OG_CHOICE_README.md  # Documentation de la page de sélection d'opérations
```

## Contenu des Documentations

### Documentation Backend Python

#### [SCRIPT_README.md](SCRIPT_README.md)
- **Point d'entrée principal** de l'application TACOS
- Orchestrateur central avec serveur Eel intégré
- Gestion de l'authentification et communication avec la base ANIS
- Logique de génération automatisée des fiches Excel
- Architecture des fonctions exposées à l'interface web

#### [QUERY_README.md](QUERY_README.md)
- **Référentiel centralisé** de toutes les requêtes SQL métier
- Extraction des données opérationnelles depuis la base ANIS
- Requêtes complexes pour Opérations Globales (OG) et Notes d'Information (NI)
- Jointures multi-tables et filtres métier sophistiqués

#### [QUERY_UTILS_README.md](QUERY_UTILS_README.md)
- **Interface de communication** avec l'API Mathis/Dremio
- Gestion de l'authentification via NNI/mot de passe
- Exécution asynchrone de requêtes SQL avec pagination
- Mécanismes de gestion d'erreurs et optimisations de performance

#### [FUNCTION_UTILS_README.md](FUNCTION_UTILS_README.md)
- **Bibliothèque d'utilitaires** pour la manipulation de données
- Gestion des couleurs Excel et validation métier
- Calculs temporels et algorithmes de positionnement
- Fonctions d'assistance pour la génération de fiches

### Documentation Frontend Web

#### Interface Utilisateur
- **[WEB/INDEX_README.md](WEB/INDEX_README.md)** : Page de connexion et authentification
- **[WEB/PAGES/FILTERS_README.md](WEB/PAGES/FILTERS_README.md)** : Interface de sélection des critères (GMR, dates)
- **[WEB/PAGES/OG_CHOICE_README.md](WEB/PAGES/OG_CHOICE_README.md)** : Page de sélection des opérations

#### Logique JavaScript
- **[WEB/JS/SCRIPT_README.md](WEB/JS/SCRIPT_README.md)** : Gestion de la connexion et communication Eel
- **[WEB/JS/FILTERS_README.md](WEB/JS/FILTERS_README.md)** : Logique des filtres GMR et validation des dates
- **[WEB/JS/EXCEL_README.md](WEB/JS/EXCEL_README.md)** : Interface de sélection et génération des fiches

#### Présentation Visuelle
- **[WEB/CSS/STYLE_README.md](WEB/CSS/STYLE_README.md)** : Feuille de style principale avec système de couleurs RTE

## Format de Documentation Standardisé

Chaque fichier de documentation suit une structure cohérente comprenant :

### 1. Aperçu du Fichier
- Type et technologie utilisée
- Position dans l'architecture TACOS
- Rôle et responsabilités principales

### 2. Fonctionnalités Principales
- Composants clés et algorithmes
- Interfaces publiques et points d'entrée
- Logique métier implémentée

### 3. Dépendances & Imports
- Bibliothèques externes requises
- Modules internes du projet
- Configuration d'environnement

### 4. Structure du Code
- Organisation hiérarchique
- Flux d'exécution principal
- Patterns d'architecture utilisés

### 5. Exemples d'Utilisation
- Cas d'usage typiques
- Extraits de code annotés
- Intégration avec d'autres composants

### 6. Configuration & Paramètres
- Variables configurables
- Paramètres par défaut
- Options de personnalisation

### 7. Notes Techniques
- Considérations de performance
- Limitations connues
- Optimisations appliquées
- Mesures de sécurité

### 8. Maintenance & Développement
- Instructions de modification
- Guidelines de contribution
- Procédures de débogage
- Fichiers associés à modifier

## Utilisation de la Documentation

### Pour les Développeurs
- **Compréhension du code** : Architecture et logique métier détaillées
- **Modification sécurisée** : Guidelines et fichiers associés à chaque changement
- **Débogage efficace** : Procédures et points de contrôle documentés
- **Extension du projet** : Patterns et exemples pour ajouter de nouvelles fonctionnalités

### Pour les Mainteneurs
- **Résolution de problèmes** : Notes techniques et limitations connues
- **Mise à jour** : Procédures de déploiement et configuration
- **Monitoring** : Considérations de performance et sécurité
- **Tests** : Recommandations de validation et scenarios de test

### Pour les Utilisateurs Avancés
- **Configuration** : Paramètres personnalisables et variables d'environnement
- **Intégration** : Interfaces d'API et exemples d'utilisation
- **Troubleshooting** : Gestion d'erreurs et cas limites

## Navigation dans la Documentation

### Liens Croisés
Chaque documentation contient des références vers les fichiers liés :
- **Modules Python** : Liens vers `script.py`, `query.py`, etc.
- **Pages Web** : Références vers `web/index.html`, `web/pages/filters.html`
- **Ressources** : Liens vers CSS, JavaScript et assets

### Index des Fonctionnalités
- **Authentification** : [WEB/INDEX_README.md](WEB/INDEX_README.md) + [SCRIPT_README.md](SCRIPT_README.md)
- **Requêtes Base de Données** : [QUERY_README.md](QUERY_README.md) + [QUERY_UTILS_README.md](QUERY_UTILS_README.md)
- **Génération Excel** : [SCRIPT_README.md](SCRIPT_README.md) + [FUNCTION_UTILS_README.md](FUNCTION_UTILS_README.md)
- **Interface Utilisateur** : `WEB/` (toutes les documentations frontend)

## Standards de Qualité

### Exhaustivité
- **100% de couverture** : Tous les fichiers source principaux documentés
- **Détails techniques** : Algorithmes, structures de données et logique métier
- **Exemples concrets** : Code fonctionnel et cas d'usage réels

### Cohérence
- **Format uniforme** : Structure identique pour tous les fichiers
- **Terminologie standardisée** : Vocabulaire cohérent à travers toute la documentation
- **Liens maintenus** : Références croisées à jour et fonctionnelles

### Maintenance
- **Mise à jour continue** : Documentation synchronisée avec les évolutions du code
- **Versioning** : Suivi des changements et historique des modifications
- **Validation** : Vérification régulière de l'exactitude technique

---

**Note :** Cette documentation constitue un référentiel vivant, régulièrement mis à jour pour refléter l'évolution du projet TACOS. Pour toute question ou suggestion d'amélioration, référez-vous aux guidelines de contribution dans chaque fichier README spécifique.