# [`web/js/excel.js`](../web/js/excel.js) - Interface de Sélection et Génération des Fiches Excel

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

### Description
Le fichier [`excel.js`](../web/js/excel.js) constitue l'interface JavaScript pour la page de sélection des opérations et génération des fiches Excel dans l'application TACOS. Il gère l'affichage dynamique des listes d'opérations globales (OG) et de notes d'information (NI), les interactions utilisateur pour la sélection multiple, et le déclenchement du processus de génération des fiches de coordination.

### Type et Technologie
- **Type** : Script JavaScript ES6+ côté client
- **Technologie** : JavaScript moderne avec DOM manipulation et communication Eel
- **Position** : Couche présentation frontend dans l'architecture [`web/js`](../web/js)

### Rôle dans l'Écosystème
Ce fichier orchestre la dernière étape de l'interface utilisateur avant la génération des fiches Excel. Il fait le pont entre les données filtrées depuis le backend Python (via Eel) et les actions utilisateur pour la sélection finale des opérations à traiter. Il communique directement avec [`script.py`](../script.py) pour récupérer les listes OG/NI et déclencher la génération Excel.

## Fonctionnalités Principales

### Communication Bidirectionnelle avec Python
Le fichier expose plusieurs fonctions au backend Python via le système Eel :

#### Fonctions Exposées (Python → JavaScript)
```javascript
eel.expose(step);
function step(message) {
  document.getElementById("indication").innerHTML = message;
  document.getElementById("container_indication").classList.remove("hidden");
}
```

#### Fonctions d'Affichage des Listes
- **`add_og_to_selection(li_og)`** : Construit dynamiquement la liste des opérations globales avec checkboxes
- **`add_ni_to_selection(li_ni)`** : Construit dynamiquement la liste des notes d'information avec checkboxes
- **`go_back(url)`** : Gère la navigation de retour vers la page précédente

### Gestion des Interfaces de Sélection Multiple

#### Construction Dynamique des Listes
```javascript
eel.expose(add_og_to_selection);
function add_og_to_selection(li_og) {
  li_og.sort();
  const ul = document.getElementById("list_og");
  for (const element of li_og) {
    const div = document.createElement("div");
    const label = document.createElement("label");
    // ... construction de l'interface checkbox + label
    div.appendChild(opt);
    div.appendChild(label);
    ul.appendChild(div);
  }
}
```

### Système de Sélection Avancé

#### Gestion des Checkboxes Individuelles
```javascript
const checkInteraction = (type) => {
  checkedBoxes = document.querySelectorAll(`input[name=${type}]:checked`).length;
  boxes = document.getElementsByClassName(type).length;
  selector = document.getElementById(`select_all_${type}`);
  selector.checked = checkedBoxes == boxes;
};
```

#### Sélection/Désélection Globale
- **`checkAllCheckbox(className)`** : Sélectionne tous les éléments d'une catégorie
- **`uncheckAllCheckbox(className)`** : Désélectionne tous les éléments d'une catégorie
- **`selectAllInteraction(classname, listType)`** : Gère l'interaction avec le bouton "Tout sélectionner"

### Fonctionnalités de Recherche et Filtrage

#### Filtrage en Temps Réel
```javascript
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
```

### Gestion des Modes d'Affichage

#### Basculement Entre OG et NI
Le script gère deux modes d'affichage exclusifs via des radio buttons :
```javascript
document.getElementById("radio_og").addEventListener("change", () => {
  if (!document.getElementById("radio_og").checked) return;
  document.getElementById("container_list_og").classList.remove("hidden");
  document.getElementById("container_list_ni").classList.add("hidden");
  // Reset de l'autre mode
});
```

## Dépendances & Imports

### Dépendances Externes
- **Eel Bridge** : `eel.js` (fourni automatiquement par le framework Eel)
  - Communication bidirectionnelle avec le backend Python
  - Exposition de fonctions JavaScript au Python
  - Appel de fonctions Python depuis JavaScript

### Dépendances DOM
- **Document Object Model** : API native du navigateur pour manipulation HTML
- **Event Listeners** : Gestion des événements utilisateur (click, change, keyup)
- **Query Selectors** : Sélection d'éléments DOM (`getElementById`, `getElementsByClassName`, `querySelectorAll`)

### Interface avec le Backend
Le script communique avec les fonctions Python suivantes :
- **`eel.get_og()`** : Récupération de la liste des opérations globales
- **`eel.get_ni()`** : Récupération de la liste des notes d'information  
- **`eel.go_back()`** : Navigation de retour
- **`eel.generate_excel(operation)`** : Déclenchement de la génération Excel

## Structure du Code

### Organisation Fonctionnelle

#### 1. Fonctions de Communication Eel (lignes 1-44)
```javascript
// Fonctions exposées au Python
eel.expose(step);
eel.expose(go_back);
eel.expose(add_og_to_selection);
eel.expose(add_ni_to_selection);
```

#### 2. Initialisation des Données (lignes 45-48)
```javascript
eel.get_og();  // Récupération des opérations globales
eel.get_ni();  // Récupération des notes d'information
```

#### 3. Variables Globales et Collections (lignes 50-52)
```javascript
const ogList = document.getElementsByClassName("og");
const niList = document.getElementsByClassName("ni");
```

#### 4. Utilitaires de Manipulation des Checkboxes (lignes 54-74)
- Fonctions de sélection/désélection en masse
- Gestion de la synchronisation des états de sélection
- Mise à jour des indicateurs visuels

#### 5. Système de Filtrage par Recherche (lignes 76-86)
```javascript
const update_selection_list_item = (li_items, input) => {
  // Filtrage case-insensitive avec masquage/affichage des éléments
};
```

#### 6. Event Listeners et Interactions (lignes 88-170)
- Gestionnaires pour les boutons "Tout sélectionner"
- Basculement entre modes OG/NI
- Recherche en temps réel dans les listes
- Navigation et génération

### Flux d'Exécution

#### Séquence d'Initialisation
1. **Chargement du script** : Exécution immédiate des appels `eel.get_og()` et `eel.get_ni()`
2. **Récupération des données** : Le backend Python retourne les listes via `add_og_to_selection()` et `add_ni_to_selection()`
3. **Construction de l'interface** : Génération dynamique des checkboxes et labels
4. **Activation des interactions** : Configuration des event listeners

#### Workflow de Sélection
1. **Affichage initial** : Mode OG activé par défaut
2. **Interaction utilisateur** : Sélection via checkboxes ou recherche
3. **Validation** : Contrôle de cohérence des sélections
4. **Génération** : Déclenchement du processus Excel via `eel.generate_excel()`

### Patterns de Conception

#### Observer Pattern
```javascript
opt.onclick = () => {
  checkInteraction("og"); // Mise à jour automatique des états
};
```

#### Factory Pattern pour Construction DOM
```javascript
// Construction standardisée des éléments de liste
const div = document.createElement("div");
const label = document.createElement("label");
const opt = document.createElement("input");
```

## Exemples d'Utilisation

### Intégration dans HTML
```html
<script type="text/javascript" src="../eel.js"></script>
<script src="../js/excel.js"></script>
```

### Structure HTML Attendue
```html
<div id="container_list_og">
  <input type="text" id="search_bar_og" placeholder="Rechercher par OG">
  <input type="checkbox" id="select_all_og"> Tout sélectionner
  <ul id="list_og"></ul>
</div>

<div id="container_list_ni" class="hidden">
  <input type="text" id="search_bar_ni" placeholder="Rechercher par NI">
  <input type="checkbox" id="select_all_ni"> Tout sélectionner
  <ul id="list_ni"></ul>
</div>
```

### Exemple d'Appel depuis Python
```python
# Dans script.py
@eel.expose
def get_og():
    return eel.add_og_to_selection(og_list)

@eel.expose  
def get_ni():
    return eel.add_ni_to_selection(ni_list)
```

### Cas d'Usage Typiques

#### Sélection Multiple d'Opérations
```javascript
// L'utilisateur peut :
// 1. Rechercher dans la liste : "OG-2024-001"
// 2. Sélectionner individuellement ou globalement
// 3. Basculer entre modes OG/NI
// 4. Déclencher la génération pour les éléments sélectionnés
```

#### Génération Excel Conditionnelle
```javascript
document.getElementById("generate_excel").onclick = () => {
  checkedBoxesog = document.querySelectorAll("input[name=og]:checked");
  checkedBoxesni = document.querySelectorAll("input[name=ni]:checked");
  
  // Génération basée sur le type majoritaire
  if (checkedBoxesog.length > checkedBoxesni.length) {
    for (const element of checkedBoxesog) {
      eel.generate_excel(element.value);
    }
  } else {
    for (const element of checkedBoxesni) {
      eel.generate_excel(element.value);
    }
  }
};
```

## Configuration & Paramètres

### Sélecteurs DOM Configurés
```javascript
// IDs des éléments requis dans le HTML
const DOM_ELEMENTS = {
  lists: {
    og: "list_og",
    ni: "list_ni"
  },
  containers: {
    og: "container_list_og", 
    ni: "container_list_ni"
  },
  searchBars: {
    og: "search_bar_og",
    ni: "search_bar_ni"  
  },
  selectAll: {
    og: "select_all_og",
    ni: "select_all_ni"
  }
};
```

### Classes CSS Utilisées
- **`.og`** : Classe appliquée aux checkboxes d'opérations globales
- **`.ni`** : Classe appliquée aux checkboxes de notes d'information
- **`.hidden`** : Classe pour masquer les éléments (définie dans style.css)

### Paramètres de Comportement
- **Tri automatique** : `li_og.sort()` et `li_ni.sort()` pour l'organisation alphabétique
- **Recherche case-insensitive** : `input.toLowerCase()` pour la tolérance de casse
- **Sélection exclusive** : Un seul mode (OG ou NI) actif à la fois

## Notes Techniques

### Performance et Optimisations

#### Manipulation DOM Optimisée
```javascript
// Construction en batch puis insertion unique
const ul = document.getElementById("list_og");
for (const element of li_og) {
  // Construction des éléments
  ul.appendChild(div); // Insertion directe sans recherche répétée
}
```

#### Event Delegation Limitée
Le script utilise des event listeners directs plutôt que de la délégation d'événements, ce qui est approprié pour des listes de taille modérée mais pourrait être optimisé pour de très grandes listes.

### Gestion d'État Robuste

#### Synchronisation des Sélections
```javascript
const checkInteraction = (type) => {
  // Calcul automatique de l'état "Tout sélectionner"
  checkedBoxes = document.querySelectorAll(`input[name=${type}]:checked`).length;
  boxes = document.getElementsByClassName(type).length;
  selector.checked = checkedBoxes == boxes;
};
```

#### Reset d'État lors du Changement de Mode
```javascript
document.getElementById("search_bar_ni").value = "";
uncheckAllCheckbox(niList);
document.getElementById("select_all_ni").checked = false;
```

### Limitations Identifiées

#### Pas de Persistance d'État
Les sélections utilisateur sont perdues lors de la navigation ou du rechargement de page.

#### Gestion d'Erreur Limitée
Pas de validation explicite des données reçues depuis le backend Python.

#### Performance sur Grandes Listes
La construction DOM synchrone pourrait ralentir l'interface avec des milliers d'opérations.

### Compatibilité Navigateur
- **ES6+ Features** : Arrow functions, const/let, template literals
- **DOM API moderne** : `querySelector`, `classList`, `addEventListener`
- **Eel Framework** : Dépendance au framework pour la communication Python

## Maintenance & Développement

### Extension du Code

#### Ajout de Nouveaux Types d'Opérations
```javascript
// Pour ajouter un type "URGENT"
eel.expose(add_urgent_to_selection);
function add_urgent_to_selection(li_urgent) {
  // Suivre le pattern des fonctions OG/NI existantes
  li_urgent.sort();
  const ul = document.getElementById("list_urgent");
  // ... construction similaire
}
```

#### Amélioration du Filtrage
```javascript
// Filtrage multicritères
const update_selection_list_item_advanced = (li_items, filters) => {
  for (const liItem of li_items) {
    const matchesAll = filters.every(filter => 
      liItem.value.toLowerCase().includes(filter.toLowerCase())
    );
    liItem.parentElement.classList.toggle("hidden", !matchesAll);
  }
};
```

### Débogage et Tests

#### Points de Contrôle Console
```javascript
// Ajout de logs pour le débogage
console.log("OG list received:", li_og);
console.log("Selection state:", {
  og: checkedBoxesog.length,
  ni: checkedBoxesni.length
});
```

#### Tests d'Intégration
```javascript
// Test de la communication Eel
if (typeof eel === 'undefined') {
  console.error('Eel bridge not loaded');
  // Fallback ou mode dégradé
}
```

### Guidelines de Contribution

#### Conventions de Nommage
- **Fonctions exposées** : Noms descriptifs en snake_case pour compatibilité Python
- **Variables DOM** : Suffixes explicites (`List`, `Container`, `Bar`)
- **Event handlers** : Noms verbaux (`checkInteraction`, `selectAllInteraction`)

#### Standards de Code
- **Cohérence** : Suivre les patterns existants pour les nouvelles fonctionnalités
- **Documentation** : Commenter les logiques complexes de manipulation DOM
- **Validation** : Ajouter des contrôles de sécurité pour les données externes

#### Tests Recommandés
- **Tests unitaires** : Validation des fonctions utilitaires de manipulation
- **Tests d'intégration** : Communication Eel avec mock du backend
- **Tests utilisateur** : Scénarios de sélection et génération complets