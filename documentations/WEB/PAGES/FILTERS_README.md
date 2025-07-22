# Documentation - filters.html

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

**Type :** Page HTML5 avec JavaScript intégré  
**Technologie :** HTML, CSS, JavaScript (avec framework Eel)  
**Position :** Interface utilisateur pour la sélection de filtres dans l'application TACOS  
**Rôle :** Page de configuration permettant à l'utilisateur de définir les paramètres de recherche (GMR, dates) avant de procéder à la sélection des opérations

### Description
Le fichier `filters.html` constitue la première étape interactive de l'application TACOS. Il permet aux utilisateurs de spécifier les critères de filtrage nécessaires pour récupérer les opérations globales (OG) et notes d'information (NI) pertinentes depuis la base de données.

## Fonctionnalités Principales

### Interface de Sélection des Filtres
- **Sélection GMR** : Champ de recherche dynamique avec autocomplétion
- **Période temporelle** : Sélection des dates de début et fin d'intervention
- **Navigation** : Redirection vers la page de sélection des opérations

### Composants Interactifs
```html
<!-- Barre de recherche GMR avec suggestions -->
<input type="text" id="gmr_search_bar" placeholder="Chercher un GMR" />
<div id="gmr_option"></div>

<!-- Sélection de période -->
<input type="date" id="date_start" required />
<input type="date" id="date_end" required />
```

### Indicateurs de Statut
- **Loader de récupération GMR** : Affichage pendant le chargement des données
- **Loader de traitement** : Indication du traitement des opérations
- **Messages d'état** : Feedback utilisateur en temps réel

## Dépendances & Imports

### Ressources Externes
```html
<!-- Framework de communication Python-JavaScript -->
<script type="text/javascript" src="../eel.js"></script>

<!-- Styles personnalisés -->
<link rel="stylesheet" href="../css/style.css" />

<!-- Scripts comportementaux -->
<script src="../js/filters.js"></script>

<!-- Favicon -->
<link rel="icon" href="../img/RTE_Logotype_interne_RVB_Bleu.svg" />
```

### Dépendances du Projet
- **style.css** : Feuille de style principale
- **filters.js** : Logique métier JavaScript
- **eel.js** : Bridge de communication avec le backend Python
- **Images RTE** : Ressources graphiques d'identité visuelle

## Structure du Code

### Architecture HTML
```html
<div class="container_all">
    <header>
        <!-- Titre de la page -->
    </header>
    
    <form action="">
        <!-- Indicateurs de chargement -->
        <div id="container_indication">...</div>
        <div id="container_indication_end">...</div>
        
        <!-- Sélection GMR -->
        <div class="solo_input" id="container_gmr">...</div>
        
        <!-- Sélection dates -->
        <div class="solo_input">...</div>
        
        <!-- Bouton de validation -->
        <button id="getfilters">...</button>
    </form>
    
    <footer></footer>
</div>
```

### Flux d'Interaction
1. **Chargement initial** : Affichage du loader GMR
2. **Récupération GMR** : Population de la liste via `filters.js`
3. **Saisie utilisateur** : Filtrage temps réel des GMR
4. **Validation** : Contrôles de cohérence des dates
5. **Traitement** : Lancement de la requête opérations
6. **Navigation** : Redirection vers `OG_choice.html`

### Gestion des États
- **État de chargement** : Classes CSS `hidden` pour contrôler l'affichage
- **État d'erreur** : Validation côté client des données
- **État de progression** : Indicateurs visuels séquentiels

## Exemples d'Utilisation

### Workflow Utilisateur Standard
```javascript
// 1. Page se charge avec récupération automatique des GMR
eel.get_gmr(); // Appelé depuis filters.js

// 2. Utilisateur tape dans la barre de recherche
document.getElementById("gmr_search_bar").addEventListener("keyup", function() {
    // Filtrage en temps réel des GMR
});

// 3. Sélection des dates et validation
document.getElementById("getfilters").onclick = () => {
    const form_data = {
        gmr: document.getElementById("gmr_search_bar").value,
        date_start: document.getElementById("date_start").value,
        date_end: document.getElementById("date_end").value,
    };
    
    // Validation et envoi
    eel.get_filters(form_data.gmr, form_data.date_start, form_data.date_end);
};
```

### Intégration avec le Backend
```python
# Fonction Python appelée depuis filters.js
@eel.expose
def get_filters(gmr, date_start, date_end):
    # Traitement des filtres et récupération des opérations
    # Redirection vers OG_choice.html
```

## Configuration & Paramètres

### Paramètres d'Interface
- **Placeholder GMR** : `"Chercher un GMR"`
- **Champs obligatoires** : Dates de début et fin marquées `required`
- **Titre de page** : `"Fiche de Coordination"`

### Classes CSS Configurables
```css
.solo_input        /* Style des champs de saisie */
.button_input      /* Style du bouton de validation */
.loader           /* Animation de chargement */
.hidden           /* Masquage conditionnel */
```

### Identifiants JavaScript
- `gmr_search_bar` : Champ de recherche GMR
- `gmr_option` : Container des suggestions
- `date_start` / `date_end` : Champs de dates
- `getfilters` : Bouton de validation
- `container_indication` : Zones de feedback

## Notes Techniques

### Considérations de Performance
- **Filtrage temps réel** : Recherche GMR sans délai de debounce
- **Chargement asynchrone** : GMR récupérés en arrière-plan
- **Validation côté client** : Contrôles immédiats sans round-trip serveur

### Patterns d'Architecture
- **Progressive Enhancement** : Fonctionnalité de base HTML avec amélioration JavaScript
- **Separation of Concerns** : Logique métier dans `filters.js`, présentation dans HTML/CSS
- **Event-Driven** : Interface réactive basée sur les événements utilisateur

### Gestion d'Erreurs
```javascript
// Validation des dates dans filters.js
if (form_data.date_start > form_data["date_end"]) {
    alert("Date de départ après date de fin");
    return;
}

// Validation du GMR sélectionné
if (!gmr_texts.includes(form_data.gmr)) {
    alert("Nom de GMR non reconnu");
    return;
}
```

### Limitations Connues
- **Dépendance Eel** : Nécessite le framework Eel pour la communication Python
- **Validation basique** : Contrôles côté client uniquement
- **GMR statiques** : Liste GMR chargée une seule fois au démarrage

## Maintenance & Développement

### Modifications Courantes
```html
<!-- Ajout d'un nouveau champ de filtre -->
<div class="solo_input">
    <label>Nouveau Filtre</label>
    <input type="text" id="nouveau_filtre" />
</div>
```

### Extension JavaScript
```javascript
// Ajout dans filters.js pour nouveau champ
document.getElementById("getfilters").onclick = () => {
    const form_data = {
        gmr: document.getElementById("gmr_search_bar").value,
        date_start: document.getElementById("date_start").value,
        date_end: document.getElementById("date_end").value,
        nouveau_filtre: document.getElementById("nouveau_filtre").value // Ajout
    };
};
```

### Tests et Debugging
- **Console Browser** : Inspection des événements JavaScript
- **Network Tab** : Monitoring des appels Eel vers Python
- **Elements Tab** : Vérification des classes CSS appliquées

### Guidelines de Contribution
1. **Validation** : Ajouter les contrôles côté client ET serveur
2. **Accessibilité** : Maintenir les labels et attributs `required`
3. **Responsive** : Tester avec les styles CSS existants
4. **Performance** : Éviter les requêtes répétées inutiles
5. **UX** : Conserver les indicateurs de progression pour les opérations longues

### Fichiers Associés à Modifier
- **filters.js** : Logique métier JavaScript
- **style.css** : Styles pour nouveaux éléments
- **script.py** : Fonctions backend Eel correspondantes
- **query.py** : Requêtes base de données pour les nouveaux filtres