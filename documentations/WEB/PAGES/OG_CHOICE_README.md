# Documentation - OG_choice.html

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
**Position :** Interface de sélection des opérations dans l'application TACOS  
**Rôle :** Deuxième étape du workflow permettant aux utilisateurs de choisir entre les Opérations Globales (OG) et les Notes d'Information (NI) pour la génération de fiches de coordination

### Description
Le fichier [`OG_choice.html`](../../../web/pages/OG_choice.html) constitue l'interface de sélection finale de l'application TACOS. Après avoir défini les filtres (GMR et dates), cette page présente les opérations disponibles sous forme de listes filtrables avec sélection multiple, permettant de générer les fiches Excel correspondantes.

## Fonctionnalités Principales

### Sélection du Type d'Intervention
- **Radio Buttons** : Choix exclusif entre OG et NI
- **Interface dynamique** : Basculement automatique entre les listes
- **État par défaut** : OG sélectionné initialement

```html
<div class="solo_input solo_radio_input">
  <div class="radio_input">
    <input name="selection" type="radio" value="og" id="radio_og" checked>
    <label>Opération Globale (OG)</label>
  </div>
</div>

<div class="solo_input solo_radio_input">
  <div class="radio_input">
    <input name="selection" type="radio" value="ni" id="radio_ni">
    <label>Note d'information (NI)</label>
  </div>
</div>
```

### Système de Recherche et Filtrage
- **Barres de recherche** : Une pour OG, une pour NI
- **Filtrage temps réel** : Recherche instantanée par nom d'opération
- **Sélection multiple** : Checkboxes pour chaque opération
- **Sélection globale** : Option "Tout sélectionner" par type

```html
<div class="container_list" id="container_list_og">
  <input type="text" class="search_bar" id="search_bar_og" placeholder="Rechercher par OG">
  <input type="checkbox" id="select_all_og" class="input_select_og_ni"> Tout selectionner </input>
  <ul id="list_og"></ul>
</div>

<div class="container_list hidden" id="container_list_ni">
  <input type="text" class="search_bar" id="search_bar_ni" placeholder="Rechercher par NI">
  <input type="checkbox" id="select_all_ni" class="input_select_og_ni"> Tout selectionner </input>
  <ul id="list_ni"></ul>
</div>
```

### Navigation et Actions
- **Bouton Retour** : Navigation vers [`filters.html`](../../../web/pages/filters.html)
- **Bouton Générer** : Lancement de la génération Excel
- **Indicateur de progression** : Loader avec messages d'état

## Dépendances & Imports

### Ressources Externes
```html
<!-- Framework de communication Python-JavaScript -->
<script type="text/javascript" src="../eel.js"></script>

<!-- Styles personnalisés -->
<link rel="stylesheet" href="../css/style.css">

<!-- Script de gestion Excel -->
<script src="../js/excel.js"></script>

<!-- Favicon -->
<link rel="icon" href="../img/RTE_Logotype_interne_RVB_Bleu.svg" />
```

### Dépendances du Projet
- **[style.css](../../../web/css/style.css)** : Feuille de style principale avec classes spécialisées
- **[excel.js](../../../web/js/excel.js)** : Logique métier JavaScript pour la gestion des opérations
- **eel.js** : Bridge de communication avec le backend Python
- **Images RTE** : Ressources d'identité visuelle corporative

### Intégration Backend
- **[script.py](../../../script.py)** : Fonctions Python exposées via Eel
- **Base de données ANIS** : Source des opérations OG/NI
- **Génération Excel** : Pipeline de traitement vers fichiers de coordination

## Structure du Code

### Architecture HTML Hiérarchique
```html
<div class="container_all">
  <header>
    <!-- Titre de section -->
  </header>
  
  <form action="">
    <!-- Sélection du type d'intervention -->
    <div class="solo_input solo_radio_input">...</div>
    
    <!-- Container de recherche dynamique -->
    <div class="container_search_bar">
      <!-- Liste OG (visible par défaut) -->
      <div class="container_list" id="container_list_og">...</div>
      
      <!-- Liste NI (masquée initialement) -->
      <div class="container_list hidden" id="container_list_ni">...</div>
    </div>
    
    <!-- Boutons d'action -->
    <div class="duo_button">...</div>
    
    <!-- Indicateur de progression -->
    <div id="container_indication" class="hidden">...</div>
  </form>
</div>
```

### Flux d'Interaction Utilisateur
1. **Chargement initial** : OG sélectionné, liste OG visible
2. **Population des listes** : Appel [`excel.js`](../../../web/js/excel.js) → `eel.get_og()` et `eel.get_ni()`
3. **Basculement radio** : Masquage/affichage conditionnel des containers
4. **Recherche temps réel** : Filtrage des éléments via JavaScript
5. **Sélection multiple** : Gestion des checkboxes individuelles et globales
6. **Génération** : Envoi des sélections au backend Python

### Mécanismes de Gestion d'État
- **Classes CSS conditionnelles** : `hidden` pour contrôler la visibilité
- **États de sélection** : Synchronisation checkbox individuelles ↔ "Tout sélectionner"
- **Nettoyage automatique** : Reset des sélections lors du basculement radio

## Exemples d'Utilisation

### Workflow Standard Utilisateur
```javascript
// 1. Page se charge, récupération automatique des opérations
eel.get_og(); // Remplit list_og via excel.js
eel.get_ni(); // Remplit list_ni via excel.js

// 2. Utilisateur bascule vers NI
document.getElementById("radio_ni").addEventListener("change", function () {
  // Cache container OG, affiche container NI
  document.getElementById("container_list_ni").classList.remove("hidden");
  document.getElementById("container_list_og").classList.add("hidden");
  
  // Reset sélections OG
  uncheckAllCheckbox(ogList);
  document.getElementById("select_all_og").checked = false;
});

// 3. Recherche dans la liste NI
document.getElementById("search_bar_ni").addEventListener("keyup", function () {
  const input = document.getElementById("search_bar_ni").value;
  update_selection_list_item(niList, input); // Filtrage temps réel
});

// 4. Génération Excel pour les éléments sélectionnés
document.getElementById("generate_excel").onclick = () => {
  checkedBoxesni = document.querySelectorAll("input[name=ni]:checked");
  for (const element of checkedBoxesni) {
    eel.generate_excel(element.value); // Appel backend Python
  }
};
```

### Intégration avec Backend Python
```python
# Fonctions exposées dans script.py
@eel.expose
def get_og():
    return eel.add_og_to_selection(og)  # Liste OG pré-filtrée

@eel.expose 
def get_ni():
    return eel.add_ni_to_selection(ni)  # Liste NI pré-filtrée

@eel.expose
def generate_excel(operation):
    # Traitement de l'opération sélectionnée
    # Génération du fichier Excel de coordination
```

## Configuration & Paramètres

### Paramètres d'Interface
- **Type par défaut** : `radio_og` coché initialement
- **Placeholders** : 
  - `"Rechercher par OG"`
  - `"Rechercher par NI"`
- **Titre de page** : `"Fiche de Coordination"`

### Identifiants JavaScript Configurables
```javascript
// Éléments de navigation
"radio_og", "radio_ni"           // Sélecteurs de type
"container_list_og", "container_list_ni"  // Containers de listes
"search_bar_og", "search_bar_ni" // Barres de recherche
"select_all_og", "select_all_ni" // Sélecteurs globaux
"list_og", "list_ni"             // Listes d'opérations

// Boutons d'action
"go_back"                        // Retour vers filters.html
"generate_excel"                 // Génération des fiches
"container_indication"           // Zone de feedback
```

### Classes CSS Spécialisées
```css
.solo_radio_input       /* Conteneur radio buttons */
.container_search_bar   /* Zone de recherche principale */
.container_list         /* Conteneur liste + recherche */
.search_bar            /* Style barre de recherche */
.input_select_og_ni    /* Checkbox "Tout sélectionner" */
.duo_button            /* Conteneur boutons Retour/Générer */
.hidden                /* Masquage conditionnel */
```

## Notes Techniques

### Considérations de Performance
- **Filtrage côté client** : Recherche instantanée sans requête serveur
- **Population différée** : Listes remplies après chargement page
- **DOM minimal** : Éléments créés dynamiquement par [`excel.js`](../../../web/js/excel.js)
- **Gestion mémoire** : Reset automatique des sélections non actives

### Patterns d'Architecture
- **Progressive Enhancement** : Fonctionnalité de base HTML + amélioration JavaScript
- **Event-Driven Design** : Interface réactive basée sur les événements utilisateur
- **State Management** : Gestion d'état explicite via classes CSS et propriétés DOM
- **Separation of Concerns** : Logique métier isolée dans [`excel.js`](../../../web/js/excel.js)

### Optimisations Appliquées
```javascript
// Filtrage optimisé avec recherche insensible à la casse
const update_selection_list_item = (li_items, input) => {
  input = input.toLowerCase();
  for (const liItem of li_items) {
    if (liItem.value.toLowerCase().includes(input)) {
      liItem.parentElement.classList.remove("hidden");
    } else {
      liItem.parentElement.classList.add("hidden");
    }
  }
};

// Synchronisation efficace des sélections
const checkInteraction = (type) => {
  checkedBoxes = document.querySelectorAll(`input[name=${type}]:checked`).length;
  boxes = document.getElementsByClassName(type).length;
  selector = document.getElementById(`select_all_${type}`);
  selector.checked = checkedBoxes == boxes;
};
```

### Limitations Connues
- **Dépendance Eel** : Nécessite framework Eel actif pour communication Python
- **Sélection exclusive** : Un seul type (OG ou NI) peut être traité à la fois
- **Pas de persistance** : Sélections perdues lors du retour navigation
- **Validation limitée** : Pas de contrôle minimum/maximum de sélections

## Maintenance & Développement

### Extension des Fonctionnalités
```html
<!-- Ajout d'un nouveau type d'opération -->
<div class="solo_input solo_radio_input">
  <div class="radio_input">
    <input name="selection" type="radio" value="nouveau_type" id="radio_nouveau">
    <label>Nouveau Type d'Opération</label>
  </div>
</div>

<!-- Container de liste correspondant -->
<div class="container_list hidden" id="container_list_nouveau">
  <input type="text" class="search_bar" id="search_bar_nouveau" placeholder="Rechercher par Nouveau">
  <input type="checkbox" id="select_all_nouveau" class="input_select_og_ni"> Tout sélectionner </input>
  <ul id="list_nouveau"></ul>
</div>
```

### Modifications JavaScript Requises
```javascript
// Dans excel.js - Ajout des event listeners
document.getElementById("radio_nouveau").addEventListener("change", () => {
  // Logique de basculement vers nouveau type
  document.getElementById("container_list_nouveau").classList.remove("hidden");
  // Masquer autres containers et reset sélections
});

// Ajout de la fonction de recherche
document.getElementById("search_bar_nouveau").addEventListener("keyup", function () {
  const input = document.getElementById("search_bar_nouveau").value;
  update_selection_list_item(nouveauList, input);
});
```

### Tests et Debugging
- **Console Browser** : Monitoring des appels Eel et gestion d'état
- **Network Tab** : Vérification des requêtes vers backend Python
- **Elements Tab** : Inspection des classes CSS appliquées dynamiquement
- **Storage Tab** : Vérification absence de persistance non voulue

### Guidelines de Contribution
1. **Cohérence UX** : Maintenir le pattern radio → container → liste → actions
2. **Performance** : Éviter les requêtes répétées, privilégier le filtrage client
3. **Accessibilité** : Conserver les labels explicites et la navigation clavier
4. **État propre** : Toujours nettoyer les sélections lors des basculements
5. **Feedback utilisateur** : Utiliser les indicateurs de progression pour les opérations longues

### Fichiers Associés à Modifier
- **[excel.js](../../../web/js/excel.js)** : Logique métier et gestion des événements
- **[script.py](../../../script.py)** : Fonctions backend Eel pour nouveaux types d'opérations
- **[style.css](../../../web/css/style.css)** : Styles pour nouveaux éléments d'interface
- **[query.py](../../../query.py)** : Requêtes base de données pour nouveaux types d'opérations

### Procédures de Débogage
```javascript
// Debug des sélections
console.log('OG sélectionnés:', document.querySelectorAll("input[name=og]:checked"));
console.log('NI sélectionnés:', document.querySelectorAll("input[name=ni]:checked"));

// Debug du filtrage
console.log('Éléments visibles OG:', 
  [...document.getElementsByClassName("og")].filter(el => 
    !el.parentElement.classList.contains("hidden")
  )
);

// Debug de la communication Eel
eel.get_og()._Promise.then(result => console.log('Données OG reçues:', result));
```