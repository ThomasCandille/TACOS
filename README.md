# Générateur de Fiches de Coordination - TACOS

## Description du projet

Ce projet est un algorithme développé pour les gestionnaires de maintenance du réseau électrique qui permet de générer automatiquement des fiches de coordination lors d'opérations impliquant plusieurs équipes. L'outil simplifie et automatise la création de documents de coordination nécessaires à la planification et au suivi des interventions sur le réseau électrique.

Le système offre une interface web permettant aux utilisateurs de sélectionner le GMR (Gestionnaire de Maintenance Régional) responsable de l'opération ainsi que la période temporelle concernée, puis génère automatiquement les fiches de coordination au format Excel.

L'objectif principal est de réduire considérablement le temps de préparation des documents de coordination tout en garantissant leur exactitude et leur conformité aux standards opérationnels du réseau électrique.

## Technologies utilisées

### Backend
- **Python** : Langage principal pour la logique métier, le traitement des données et la génération des fichiers Excel. 
- **xlwings** : Bibliothèque Python pour la manipulation avancée des fichiers Excel avec préservation du formatage. Permet de maintenir la mise en forme des templates Excel existants tout en automatisant la saisie des données.
- **requests** : Gestion des requêtes HTTP vers l'API Dremio pour récupérer les données. Bibliothèque standard pour les communications API REST.
- **datetime** : Manipulation des dates et calculs temporels. Essentiel pour la gestion des périodes d'intervention et la conversion des formats de dates.
- **json** : Traitement des réponses JSON de l'API Dremio
- **time** : Gestion des délais et temporisation lors des requêtes asynchrones
- **urllib3** : Configuration des paramètres de sécurité SSL pour les connexions API

### Frontend
- **HTML/CSS** : Structure et stylisation de l'interface utilisateur.
- **JavaScript** : Logique côté client et interaction utilisateur. Gère la navigation entre les pages, la validation des formulaires et les interactions dynamiques.
- **Eel** : Bridge entre Python et JavaScript permettant l'exécution de fonctions Python depuis le frontend. Cette technologie hybride permet de combiner la puissance de Python avec la flexibilité d'une interface web.

### Base de données
- **Dremio** : Plateforme de virtualisation de données utilisée pour accéder aux informations du réseau électrique via une API REST. Dremio permet d'unifier l'accès à plusieurs sources de données hétérogènes tout en offrant une interface SQL standard.

## Prérequis - Accès à la base de données

Le système utilise **Dremio** comme plateforme de données pour récupérer les informations relatives aux opérations, équipes et ouvrages du réseau électrique. **Il est impératif de disposer des accès authentifiés à cette base de données** pour pouvoir utiliser l'application. 

Les requêtes de connexion nécessitent des identifiants valides (NNI et mot de passe) pour s'authentifier auprès de l'API Dremio. L'authentification génère un token JWT temporaire utilisé pour toutes les requêtes subséquentes. Le système gère automatiquement les erreurs d'authentification (401, 403, 404) et informe l'utilisateur en cas de problème de connexion.

## Arborescence du projet

```
TACOS/
├── web/                          # Interface utilisateur web
│   ├── index.html               # Page de connexion principale
│   ├── pages/                   # Pages additionnelles de l'application
│   │   ├── filters.html         # Interface de sélection GMR et période
│   │   └── OG_choice.html       # Page de choix des opérations
│   ├── css/                     # Feuilles de style
│   │   └── style.css           # Styles globaux de l'application
│   ├── js/                      # Scripts JavaScript
│   │   ├── script.js           # Logique de connexion et navigation
│   │   ├── filters.js          # Gestion des filtres GMR/dates
│   │   └── excel.js            # Sélection OG/NI et génération Excel
│   ├── fonts/                  # Polices personnalisées
│   ├── img/                    # Ressources graphiques (logos RTE)
├── script.py                   # Point d'entrée principal de l'application
├── function_utils.py           # Fonctions utilitaires transversales
├── query.py                    # Définition des requêtes SQL Dremio
├── query_utils.py              # Utilitaires de connexion et exécution API
├── TEMPLATE.xlsm               # Modèle de fichier Excel pour la génération des fiches
├── TacosManuelTEMPLATE.xlsm    # Modele de fichier Excel pour la création manuelle des fiches
└── README.md                   # Documentation du projet
```

## Le package Eel

**Eel** est une bibliothèque Python qui permet de créer des applications de bureau avec des interfaces web en établissant un pont entre Python et JavaScript. Cette approche hybride offre plusieurs avantages dans ce projet :

### Fonctionnalités d'Eel dans TACOS :
- **Exécution bidirectionnelle** : Les fonctions Python peuvent être appelées directement depuis JavaScript via `eel.fonction_python()` et inversement avec `eel.fonction_js()`
- **Interface moderne** : Permet de créer une interface utilisateur moderne en HTML/CSS/JS tout en conservant la puissance de Python pour la logique métier complexe
- **Application autonome** : Lance l'application dans une fenêtre de navigateur dédiée, créant une expérience d'application de bureau
- **Communication en temps réel** : Les fonctions Python exposées via `@eel.expose` deviennent accessibles côté JavaScript, permettant une communication bidirectionnelle fluide
- **Simplicité de déploiement** : Une seule application contenant frontend et backend, facile à distribuer

### Architecture de communication :
```
JavaScript (Frontend) ↔ Eel Bridge ↔ Python (Backend) ↔ API Dremio
```

## Description détaillée des fichiers

### script.py - Point d'entrée principal

**Rôle central :** Ce fichier constitue le cœur de l'application, orchestrant tous les processus depuis l'authentification jusqu'à la génération des fiches Excel.

**Fonctionnalités principales :**
- **Initialisation Eel** : Configuration et démarrage de l'application avec `eel.init("web")` et `eel.start()`
- **Gestion globale des variables** : Maintien des états de session (headers d'authentification, listes OG/NI, GMR sélectionné)
- **Orchestration des workflows** : Coordination des différentes étapes du processus de génération
- **Interface API-Frontend** : Exposition des fonctions Python au frontend via les décorateurs `@eel.expose`

**Fonctions exposées détaillées :**

- **`get_data(nni, mdp)`** : 
  - Gère l'authentification utilisateur via l'API Dremio
  - Stocke les headers d'authentification pour les requêtes ultérieures
  - Retourne les codes d'erreur appropriés en cas d'échec de connexion
  
- **`get_gmr()`** : 
  - Récupère la liste complète des GMR disponibles depuis la base de données
  - Transmet les données au frontend via `eel.display_gmr()`
  - Gère les erreurs de requête et les timeouts
  
- **`get_filters(gmr, date_start, date_end)`** : 
  - Exécute le filtrage complexe des opérations selon les critères utilisateur
  - Traite et valide les opérations selon les règles métier
  - Sépare les opérations globales (OG) des notes d'information (NI)
  - Optimise les performances avec des structures de données déduplicatrices
  
- **`get_og()` / `get_ni()`** : 
  - Transmettent les listes filtrées d'opérations au frontend
  - Gèrent la navigation entre les différentes vues
  
- **`generate_excel(operation)`** : 
  - Point culminant du processus : génère les fiches Excel complètes
  - Intègre toutes les données d'opération, équipes et planification
  - Applique le formatage et la mise en forme selon les standards

### function_utils.py - Fonctions utilitaires

**Rôle :** Bibliothèque de fonctions utilitaires spécialisées pour les calculs, validations et manipulations de données spécifiques au domaine métier.

**Catégories de fonctionnalités :**

#### Gestion des couleurs et formatage Excel
- **`get_background_color(code, sheet)`** : 
  - Associe automatiquement une couleur de fond selon le type d'équipe
  - Mapping prédéfini : STAIA (bleu), STGP (rouge), STEL (gris), STEC (violet), STEPP (gris clair)
  - Met à jour les cellules de référence dans la feuille Excel pour activer les légendes

#### Calculs temporels et calendaires
- **`get_operation_day_number(operation_date)`** : 
  - Convertit une date d'opération (format ISO) en numéro de jour dans l'année (1-366)
  - Utilise `strftime("%j")` pour le calcul du jour julien
  - Essentiel pour le positionnement temporel sur les plannings annuels

- **`days_in_year(year)`** : 
  - Calcule précisément le nombre de jours dans une année donnée
  - Gère automatiquement les années bissextiles
  - Utilise les objets `datetime.date` pour les calculs exacts

#### Utilitaires Excel avancés
- **`getColumn(index)`** : 
  - Convertit un index numérique en référence de colonne Excel (H, I, J... Z, AA, AB...)
  - Gère la transition des colonnes simples (A-Z) vers les colonnes doubles (AA-ZZ)
  - Calcul basé sur les valeurs ASCII avec gestion des débordements

#### Extraction et validation des données d'opération
- **`get_element_of_operation(operations)`** : 
  - Extrait systématiquement les noms et types des parties prenantes d'une liste d'opérations
  - Retourne deux listes parallèles pour faciliter les traitements ultérieurs
  - Gère les structures de données complexes des opérations

- **`get_occurence_of_element(list_equipe)`** : 
  - Analyse la diversité des équipes impliquées dans une opération
  - Utilise des `set` pour détecter la présence de codes d'équipes distincts
  - Filtre automatiquement les valeurs `None` pour éviter les erreurs

#### Validation métier complexe
- **`is_operation_valid(operation, list_equipe)`** : 
  - Applique un ensemble de règles métier complexes pour valider une opération
  - Critères de validation :
    - `isNotPartiePrenante` : Exclut les sociétés tierces
    - `isMoreThanOne` : Nécessite plusieurs parties prenantes
    - `isNotAlone` : Vérifie la présence de plusieurs équipes
    - `isNotDI` : Exclut les opérations CDI (Contrôle Des Installations)
  - Retourne un booléen de validation globale

- **`isEquipeHere(row)`** : 
  - Vérifie la complétude des informations d'équipe dans une ligne de données
  - Contrôle la présence des champs `NOM` et `CODE_TB14`
  - Validation préalable avant traitement des données d'équipe

### query.py - Requêtes Dremio

**Rôle :** Centralise toutes les requêtes SQL vers la base de données Dremio, optimisées pour les performances et la lisibilité.

**Architecture des chemins de données :**
- **Base intégration** : `"PUBLIC".ANIS."REC_ANIS".ANIS."TBxxx"`
- **Base production** : `"PRIV_ANIS".INPUT.ANIS."PROD_ANIS".ANIS."TBxxx"`
- **Base publique** : `"PUBLIC".ANIS."TBxxx"`

**Requêtes principales détaillées :**

- **`query_to_get_gmr()`** : 
  - Requête simple récupérant tous les GMR uniques depuis TB009_GMR
  - Base de données : Production
  - Optimisée avec `DISTINCT` pour éviter les doublons

- **`query_to_get_og_ni(date_end, date_start, gmr)`** : 
  - Requête complexe multi-tables pour filtrer les opérations
  - Jointures multiples entre tables d'opérations, équipes et dates
  - Filtrage temporel précis sur les périodes d'intervention
  - Restriction par GMR pour cibler les opérations pertinentes

- **`query_get_operation_intervention(operation)`** : 
  - Récupère les détails complets d'une opération spécifique
  - Inclut les informations d'équipes, ouvrages et planning
  - Jointures optimisées pour minimiser les temps de réponse

- **`query_get_equipes_pilotes(gmr)`** / **`query_get_equipes_intervenantes(numero_ni)`** : 
  - Requêtes spécialisées pour les différents types d'équipes
  - Distinction entre équipes pilotes (coordination) et intervenantes (exécution)
  - Filtrage par GMR ou numéro de NI selon le contexte

- **`query_get_id_og_from_numero_og(numero_og)`** / **`query_get_id_og_from_numero_ni(numero_ni)`** : 
  - Requêtes de résolution d'identifiants
  - Conversion entre numéros métier et identifiants techniques
  - Essentielles pour les jointures et références croisées

### query_utils.py - Utilitaires de connexion

**Rôle :** Gère l'interface complète avec l'API Dremio, de l'authentification à l'exécution des requêtes complexes.

**Configuration du serveur :**
- **Serveur de production / public** : `mathis.rte-france.com`
- **Serveur d'intégration** : `mathis-integration.rte-france.com`
- **Sécurité SSL** : Désactivée pour l'environnement interne (`USE_SSL_VERIFICATION = False`)

**Fonctions clés détaillées :**

#### Authentification et sécurité
- **`get_headers(nni, mdp)`** : 
  - **Processus d'authentification complet** :
    1. Envoi des credentials au endpoint `/apiv2/login`
    2. Récupération du token JWT de session
    3. Construction des headers d'autorisation avec format `_dremio{authToken}`
    4. Gestion complète des codes d'erreur HTTP (401, 403, 404)
  - **Valeurs de retour** : Tuple (headers, status_code_response) pour gestion d'erreur
  - **Sécurité** : Désactivation des warnings SSL pour environnement interne

#### Exécution de requêtes asynchrones
- **`make_query(query, headers)`** : 
  - **Workflow complet d'exécution** :
    1. **Soumission** : POST de la requête SQL au endpoint `/api/v3/sql`
    2. **Monitoring** : Polling du statut du job via `/api/v3/job/{jobId}`
    3. **Attente active** : Boucle avec temporisation (0.4s) jusqu'à completion
    4. **Récupération** : GET des résultats via `/api/v3/job/{jobId}/results`
    5. **Pagination automatique** : Gestion des résultats > 500 lignes avec offset/limit
  
  - **États de job gérés** : 
    - `RUNNING` : En cours d'exécution
    - `COMPLETED` : Terminé avec succès
    - `FAILED` : Échec de l'exécution
    - `CANCELED` : Annulé par le système
  
  - **Optimisations** :
    - Pagination automatique par blocs de 500 résultats
    - Temporisation adaptative pour éviter la surcharge serveur
    - Gestion des timeouts et reconnexions automatiques

### Fichiers JavaScript - Interface utilisateur

#### script.js - Gestion de la connexion
**Fonctionnalités principales :**
- **Redimensionnement dynamique** : Adaptation de la fenêtre selon le contenu affiché
- **Validation de formulaire** : Contrôle des champs NNI et mot de passe avant soumission
- **Communication Eel** : Interface avec les fonctions Python d'authentification
- **Gestion d'erreurs** : Affichage des messages d'erreur de connexion à l'utilisateur
- **Navigation** : Transition vers la page de filtres après authentification réussie

#### filters.js - Sélection GMR et période
**Fonctionnalités avancées :**
- **Affichage dynamique des GMR** : Réception et rendu de la liste depuis `get_gmr()`
- **Recherche en temps réel** : Filtrage instantané de la liste des GMR avec barre de recherche
- **Validation temporelle** : Contrôle de cohérence des dates début/fin
- **Interface responsive** : Adaptation aux différentes tailles d'écran
- **Transmission de données** : Envoi des critères sélectionnés vers `get_filters()`

#### excel.js - Sélection et génération
**Fonctionnalités complexes :**
- **Gestion des listes multiples** : Affichage séparé des OG et NI avec compteurs
- **Recherche et filtrage** : Fonctionnalités de recherche instantanée dans les listes
- **Sélection multiple** : Interface de sélection avec checkboxs et sélection globale
- **Indicateurs visuels** : Badges de comptage et statuts de sélection
- **Génération Excel** : Déclenchement du processus de génération avec feedback utilisateur
- **Gestion des états** : Sauvegarde des sélections utilisateur et navigation

### Fichiers HTML et CSS - Présentation

#### index.html - Page de connexion
**Structure et fonctionnalités :**
- **Design centré** : Interface de connexion
- **Formulaire sécurisé** : Champs NNI et mot de passe avec validation
- **Intégration Eel** : Inclusion du script bridge `eel.js` pour communication Python
- **Accessibilité** : Labels appropriés et navigation clavier optimisée

#### filters.html - Sélection des critères
**Interface avancée :**
- **Sélection GMR** : Liste déroulante avec recherche intégrée
- **Sélecteur de dates** : Widgets de dates avec validation de plages
- **Feedback utilisateur** : Indicateurs de chargement et messages de statut
- **Navigation fluide** : Boutons de retour et progression

#### OG_choice.html - Choix des opérations
**Interface de sélection complexe :**
- **Listes multiples** : Affichage séparé et simultané des OG et NI
- **Outils de recherche** : Barres de recherche dédiées pour chaque liste
- **Sélection en masse** : Fonctionnalités de sélection/désélection globale
- **Compteurs dynamiques** : Affichage en temps réel du nombre d'éléments sélectionnés
- **Validation** : Contrôle de cohérence avant génération

#### style.css - Stylisation complète
**Design system complet :**
- **Identité visuelle RTE** : Respect de la charte graphique avec couleurs et polices officielles
- **Animations CSS** : Transitions fluides et indicateurs de chargement animés
- **États interactifs** : Hover, focus et active states pour tous les éléments interactifs
- **Accessibilité** : Contrastes conformes WCAG et support des technologies d'assistance

### Template Excel - TEMPLATE.xlsm
**Rôle :** Modèle de fichier Excel utilisé pour la génération des fiches de coordination
- **Structure prédéfinie** : Feuilles et colonnes formatées pour accueillir les données d'opération
- **Mise en forme conditionnelle** : Couleurs et styles appliqués automatiquement selon les types d'équipes
- **Formules intégrées** : Formules pour modifications du calendrier
- **Macros VBA** : Automatisations spécifiques pour la génération des fiches, comme le formatage et l'insertion de données

## Processus de génération des fiches

### Workflow complet :
1. **Authentification** : Connexion à l'API Dremio avec credentials utilisateur
2. **Sélection GMR** : Choix du gestionnaire de maintenance régional
3. **Filtrage temporel** : Définition de la période d'intervention
4. **Récupération des données** : Extraction des opérations correspondantes
5. **Validation métier** : Application des règles de coordination
6. **Sélection utilisateur** : Choix final des opérations à traiter
7. **Génération Excel** : Création automatique des fiches formatées

### Nomenclature des fichiers générés :
- **Format** : `NI_{numero_ni}_S{semaine_debut}-{semaine_fin}_{localisation}.xlsx`
- **Répertoire** : `ficheExcel/` dans le dossier racine du projet
- **Contenu** : Fiche de coordination complète avec planification, équipes et ouvrages concernés

Le système garantit la traçabilité complète du processus et la conformité des documents générés aux standards opérationnels

## Output de la console d'execution

Lors de l'exécution du script, la console affichera les données des requetes SQL Dremio, les erreurs éventuelles et les étapes de progression. Les information y seront en brut.