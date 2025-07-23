# README - filters.js

## Table des Matières
1. [Aperçu du Fichier](#1-aperçu-du-fichier)
2. [Fonctionnalités Principales](#2-fonctionnalités-principales)
3. [Dépendances & Imports](#3-dépendances--imports)
4. [Structure du Code](#4-structure-du-code)
5. [Exemples d'Utilisation](#5-exemples-dutilisation)
6. [Configuration & Paramètres](#6-configuration--paramètres)
7. [Notes Techniques](#7-notes-techniques)
8. [Maintenance & Développement](#8-maintenance--développement)

## 1. Aperçu du Fichier

**Type de fichier :** JavaScript côté client  
**Technologie :** JavaScript ES6+ avec intégration Eel (Python-JavaScript bridge)  
**Position dans l'architecture :** Module frontend pour la gestion des filtres GMR et dates dans l'application TACOS  
**Fichier :** [`web/js/filters.js`](../web/js/filters.js)

### Description
Ce fichier implémente la logique d'interface utilisateur pour la page de sélection des filtres GMR et de périodes temporelles. Il sert d'intermédiaire entre l'interface utilisateur et le backend Python via le framework Eel.

### Rôle dans l'écosystème
- **Interface de filtrage :** Première étape du workflow utilisateur pour sélectionner les critères de recherche
- **Validation des données :** Contrôle de cohérence des entrées utilisateur (dates, GMR valides)
- **Communication bidirectionnelle :** Pont entre l'interface web et les services Python backend
- **Navigation :** Gestion des transitions entre les pages de l'application

## 2. Fonctionnalités Principales

### Fonctions Exposées à Python (Eel)
```javascript
eel.expose(display_gmr);
function display_gmr(li_GMR) // Lignes 7-18
```
Affiche la liste des GMR récupérés depuis le backend dans l'interface utilisateur.

```javascript
eel.expose(go_to);
function go_to(url) // Lignes 20-22
```
Gère la navigation entre les pages de l'application.

### Fonctions Utilitaires
```javascript
const update_selection_list_items = (list_gmr, input) // Lignes 26-33
```
Filtre dynamiquement les éléments GMR selon la saisie utilisateur.

```javascript
const update_search_bar_text = (search_bar, val, list_gmr) // Lignes 35-38
```
Met à jour la barre de recherche et applique le filtrage correspondant.

### Gestionnaires d'Événements
- **Recherche GMR :** Filtrage en temps réel lors de la saisie (lignes 40-44)
- **Sélection GMR :** Mise à jour automatique du champ de recherche lors du clic (lignes 13-15)
- **Validation formulaire :** Contrôles de cohérence avant soumission (lignes 46-64)

### Logique de Validation
```javascript
if (form_data.date_start > form_data["date_end"]) {
    alert("Date de départ après date de fin");
    return;
}
```
Validation de la cohérence temporelle des dates sélectionnées.

```javascript
if (!gmr_texts.includes(form_data.gmr)) {
    alert("Nom de GMR non reconnu");
    return;
}
```
Vérification que le GMR saisi existe dans la liste autorisée.

## 3. Dépendances & Imports

### Dépendances Externes
- **Eel Framework :** Communication Python-JavaScript bidirectionnelle
  - Fonctions appelées : `eel.get_gmr()`, `eel.get_filters()`
  - Fonctions exposées : `display_gmr()`, `go_to()`

### Dépendances DOM
- **HTML Elements requis :**
  - `#gmr_option` : Container pour la liste des GMR
  - `#gmr_search_bar` : Champ de saisie GMR
  - `#date_start`, `#date_end` : Champs de sélection de dates
  - `#getfilters` : Bouton de validation
  - `#container_indication`, `#container_indication_end` : Indicateurs de chargement

### Fichiers Associés
- **HTML :** [`filters.html`](../../../web/pages/filters.html) - Interface utilisateur correspondante
- **CSS :** [`style.css`](../../../web/css/style.css) - Styles pour les classes `.gmr`, `.hidden`
- **Backend :** Fonctions Python `get_gmr()` et `get_filters()` via Eel

## 4. Structure du Code

### Flux d'Exécution Principal
1. **Initialisation :** Appel automatique `eel.get_gmr()` au chargement (ligne 3)
2. **Réception des données :** `display_gmr()` peuple l'interface avec les GMR disponibles
3. **Interaction utilisateur :** Filtrage temps réel et sélection GMR
4. **Validation :** Contrôles de cohérence avant transmission
5. **Soumission :** Envoi des filtres au backend via `eel.get_filters()`

### Organisation Fonctionnelle
```
Initialisation
├── eel.get_gmr() → Backend Python
├── display_gmr() ← Reception des GMR
└── Event Listeners Setup

Interactions Utilisateur
├── Recherche GMR (keyup)
├── Sélection GMR (click)
└── Validation Formulaire (click)

Validation & Soumission
├── Validation dates
├── Validation GMR
└── Transmission backend
```

### Gestion d'État
- **Variables globales :** `gmr` (collection d'éléments DOM)
- **État UI :** Classes CSS `hidden` pour la visibilité des éléments
- **Données formulaire :** Collecte dynamique lors de la soumission

### Mécanismes de Gestion d'Erreurs
- **Alertes utilisateur :** Messages d'erreur explicites pour dates incohérentes et GMR invalides
- **Validation préventive :** Contrôles côté client avant transmission backend
- **Filtrage défensif :** Conversion en minuscules pour la recherche insensible à la casse

## 5. Exemples d'Utilisation

### Initialisation dans une Page HTML
```html
<script type="text/javascript" src="../eel.js"></script>
<script src="../js/filters.js"></script>
```

### Structure HTML Requise
```html
<div id="container_gmr">
    <input type="text" id="gmr_search_bar" placeholder="Chercher un GMR" />
    <div id="gmr_option"></div>
</div>
<input type="date" id="date_start" required />
<input type="date" id="date_end" required />
<button id="getfilters">Suivant</button>
```

### Utilisation Côté Python
```python
@eel.expose
def get_gmr():
    # Récupération des GMR depuis la base de données
    li_gmr = ["GMR_NORD", "GMR_SUD", "GMR_EST", "GMR_OUEST"]
    eel.display_gmr(li_gmr)

@eel.expose  
def get_filters(gmr, date_start, date_end):
    # Traitement des filtres reçus
    # Redirection vers la page suivante
    eel.go_to('./OG_choice.html')
```

### Scenario d'Utilisation Typique
1. L'utilisateur accède à la page de filtres
2. La liste des GMR se charge automatiquement
3. L'utilisateur tape dans la barre de recherche → filtrage en temps réel
4. L'utilisateur clique sur un GMR → sélection automatique
5. L'utilisateur sélectionne les dates de début et fin
6. L'utilisateur clique "Suivant" → validation et transition

## 6. Configuration & Paramètres

### Paramètres de Recherche
- **Filtrage GMR :** Recherche insensible à la casse via `toLowerCase()`
- **Validation temporelle :** Comparaison directe des valeurs de dates

### Classes CSS Utilisées
```javascript
element.classList.remove("hidden");  // Affichage d'élément
element.classList.add("hidden");     // Masquage d'élément
```

### Sélecteurs DOM Configurés
- `#gmr_search_bar` : Champ de recherche principal
- `#gmr_option` : Container dynamique pour les options
- `#date_start`, `#date_end` : Champs de sélection temporelle
- `#getfilters` : Déclencheur de validation
- `#container_indication*` : Indicateurs d'état

### Paramètres de Navigation
- **URL de redirection :** `./OG_choice.html` (page suivante du workflow)
- **Structure des données :** Format attendu `{gmr, date_start, date_end}`

## 7. Notes Techniques

### Considérations de Performance
- **Filtrage optimisé :** Utilisation d'événements `keyup` avec filtrage DOM direct
- **Recherche efficace :** Conversion en minuscules unique par recherche
- **DOM manipulation :** Création d'éléments réutilisables avec event listeners

### Mesures de Sécurité
- **Validation côté client :** Double vérification des données avant transmission
- **Sanitisation implicite :** Vérification d'appartenance à la liste autorisée des GMR
- **Prévention d'injection :** Utilisation de `innerHTML` contrôlée avec données validées

### Limitations Identifiées
- **Dépendance Eel :** Fonctionnement conditionné à la disponibilité du backend Python
- **Validation limitée :** Absence de validation format de date avancée
- **Gestion d'erreur basique :** Alertes simples sans retry ou recovery

### Optimisations Appliquées
```javascript
const gmr_texts = [...gmr].map(element => element.innerHTML);
```
Utilisation de spread operator et map pour une conversion efficace des éléments DOM.

### Patterns d'Architecture
- **Event-driven :** Architecture basée sur les événements DOM
- **Separation of Concerns :** Séparation claire entre logique UI et communication backend
- **Progressive Enhancement :** Fonctionnalités activées post-chargement des données

## 8. Maintenance & Développement

### Instructions pour Modification
1. **Ajout de nouveaux champs :** Étendre l'objet `form_data` lignes 46-50
2. **Modification validation :** Adapter les conditions lignes 52-60
3. **Changement de navigation :** Modifier l'URL ligne 64

### Extensions Possibles
- **Validation de date avancée :** Intégration de bibliothèques comme moment.js
- **Autocomplétion améliorée :** Algorithmes de recherche floue
- **Gestion d'erreur robuste :** Mécanismes de retry et notifications utilisateur

### Debugging
```javascript
console.log(gmr_texts); // Vérification des GMR disponibles
console.log(form_data); // Debug des données formulaire
```

### Points d'Attention pour le Développement
- **Cohérence des ID :** Maintenir la correspondance entre JS et HTML
- **Gestion d'état :** Surveiller la synchronisation avec les classes CSS
- **Communication Eel :** Tester la disponibilité des fonctions backend

### Tests Recommandés
- **Test de filtrage :** Vérifier le comportement avec différentes saisies
- **Test de validation :** Contrôler les cas limites de dates
- **Test d'intégration :** Valider la communication avec le backend Python
- **Test de navigation :** Confirmer les transitions entre pages

### API Interne
```javascript
// Fonctions publiques exposées à Python
display_gmr(li_GMR)     // Affichage des GMR
go_to(url)              // Navigation

// Fonctions utilitaires internes  
update_selection_list_items(list_gmr, input)  // Filtrage
update_search_bar_text(search_bar, val, list_gmr)  // Mise