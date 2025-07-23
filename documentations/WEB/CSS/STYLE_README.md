# TACOS - Style.css Documentation

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
Le fichier `style.css` est la feuille de style principale de l'application TACOS. Il fournit l'ensemble des styles visuels pour une interface utilisateur.

### Type et Technologie
- **Type** : Feuille de style CSS3
- **Langage** : CSS (Cascading Style Sheets)
- **Version** : CSS3 avec propriétés modernes

### Position dans l'Architecture
Ce fichier CSS est le style principal référencé par toutes les pages HTML du projet :
- `index.html` - Page de connexion
- `filters.html` - Page de sélection GMR et dates
- `OG_choice.html` - Page de choix d'opérations

### Rôle et Responsabilités
- Définition de l'apparence visuelle complète de l'application
- Gestion du layout responsive
- Standardisation des composants d'interface (boutons, formulaires, loaders)
- Implémentation du système de couleurs RTE

## Fonctionnalités Principales

### Reset CSS Complet
```css
/* Reset CSS universel */
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}
```

### Système de Typographie
```css
@font-face {
  font-family: "Nunito";
  src: url("../fonts/NunitoSans-Regular.ttf");
}
```

### Composants d'Interface Principaux
1. **Container Principal** : Layout fixe
2. **Formulaires** : Styles pour inputs, radios, checkboxes
3. **Boutons** : Système de boutons avec états hover/active
4. **Listes déroulantes** : Styles pour les sélecteurs avec scroll
5. **Loader animé** : Animation CSS pour les états de chargement

### Animations et Effets
- Loader animé avec keyframes
- Transitions hover sur les boutons
- États visuels pour les interactions utilisateur

## Dépendances & Imports

### Ressources Externes
```css
/* Police personnalisée Nunito */
@font-face {
  font-family: "Nunito";
  src: url("../fonts/NunitoSans-Regular.ttf");
}
```

### Images de Fond
```css
background-image: url("../img/eolienneautre.png");
```

### Structure des Dépendances
- **Fonts** : `/fonts/NunitoSans-Regular.ttf`
- **Images** : `/img/eolienneautre.png` (image de fond page connexion)
- **Aucune dépendance CSS externe**

## Structure du Code

### Organisation Hiérarchique

#### 1. Reset CSS
Reset complet de tous les éléments HTML.

#### 2. Styles de Base
```css
body {
  height: 100vh;
  font-family: Nunito, sans-serif;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #eeeeee;
}
```

#### 3. Layout Principal
```css
.container_all {
  width: 375px;
  height: 677px;
  background-color: white;
  border-radius: 5px;
}
```

#### 4. Composants Spécialisés
- **Page de Connexion** : Styles spécifiques avec image de fond
- **Header** : Branding
- **Formulaires** : Styles complets pour tous les types d'inputs
- **Boutons** : Système de boutons avec variantes

#### 5. Composants Avancés
- **Listes de Sélection** : Scrollables avec interactions
- **Loader Animé** : Animation CSS
- **Classes Utilitaires** : `.hidden`, `.container_button`, etc.

### Flux d'Exécution
1. Reset de tous les styles par défaut
2. Application des styles de base (body, container)
3. Styles spécifiques par page/composant
4. États interactifs et animations

## Exemples d'Utilisation

### Intégration dans HTML
```html
<link rel="stylesheet" href="../css/style.css" />
```

### Structure de Page Type
```html
<div class="container_all">
  <header>
    <p class="header-text">Titre de la Page</p>
  </header>
  
  <form action="">
    <div class="solo_input">
      <input type="text" placeholder="Champ de saisie" />
    </div>
    
    <button class="button_input">Action</button>
  </form>
  
  <footer></footer>
</div>
```

### Utilisation des Classes Principales
```html
<!-- Input simple -->
<div class="solo_input">
  <input type="text" id="exemple" />
</div>

<!-- Radio button -->
<div class="solo_input solo_radio_input">
  <div class="radio_input">
    <input type="radio" name="choix" />
    <label>Option</label>
  </div>
</div>

<!-- Boutons -->
<button class="button_input">Bouton Principal</button>
<button id="go_back">Retour</button>

<!-- Loader -->
<div id="container_indication">
  <div class="loader"></div>
  <div id="indication">Message...</div>
</div>
```

## Configuration & Paramètres

### Couleurs Principales
```css
/* Couleur principale RTE */
background-color: #3d70ad;
border: 1px solid #3d70ad;

/* Couleurs d'état */
background-color: #2f5d9a; /* Hover */
background-color: #274a7d; /* Active */
background-color: #eeeeee; /* Fond général */
```

### Dimensions Fixes
```css
/* Container principal */
width: 375px;
height: 677px;

/* Hauteurs des sections */
header { height: 15%; }
form { height: 80%; }
footer { height: 10%; }
```

### Paramètres de Police
```css
font-family: Nunito, sans-serif;
font-size: 28px; /* Titres */
font-weight: bold;
line-height: 120%;
```

### États des Couleurs de Statut
```css
/* Couleurs pour les statuts d'opération */
color: blue;      /* Diffusée */
color: lightgray; /* Sans Objet */
color: orange;    /* En construction */
color: green;     /* Validée */
```

## Notes Techniques

### Considérations de Performance
- **Fonts locales** : Utilisation de fonts hébergées localement pour éviter les requêtes externes
- **Animations CSS** : Animations pures CSS sans JavaScript pour de meilleures performances
- **Sélecteurs optimisés** : Utilisation de classes spécifiques plutôt que de sélecteurs complexes

### Compatibilité
- **CSS3** : Utilisation de propriétés modernes (flexbox, border-radius, box-shadow)
- **Cross-browser** : Reset CSS complet pour assurer la cohérence

### Limitations
- **Overflow hidden** : Peut causer des problèmes sur petits écrans

### Mesures de Sécurité
- **Pas de contenu externe** : Toutes les ressources sont locales
- **Validation CSS** : Structure respectant les standards W3C

### Optimisations Appliquées
```css
/* Désactivation des warnings de sécurité */
filter: drop-shadow(0 0 0.5rem #6f767baa);

/* Animation optimisée */
mix-blend-mode: darken;
filter: blur(4px) contrast(10) hue-rotate(270deg);
```

## Maintenance & Développement

### Instructions de Modification

#### Ajout de Nouveaux Composants
1. Suivre la structure existante avec classes `.component_name`
2. Respecter les dimensions du container
3. Utiliser les couleurs RTE définies

#### Modification des Couleurs
```css
/* Modifier ces variables pour changer le thème */
#3d70ad /* Bleu principal RTE */
#2f5d9a /* Bleu hover */
#274a7d /* Bleu active */
```

#### Extension du Système de Boutons
```css
/* Template pour nouveaux boutons */
.nouveau_bouton {
  display: inline-flex;
  height: 32px;
  padding: 8px 16px;
  justify-content: center;
  align-items: center;
  /* Ajouter styles spécifiques */
}
```

### Procédures de Débogage
1. **Vérifier les chemins des ressources** : Fonts et images
2. **Tester les animations** : Performances du loader

### Guidelines de Contribution
- **Cohérence** : Respecter la nomenclature existante des classes
- **Performance** : Éviter les sélecteurs complexes
- **Accessibilité** : Maintenir les contrastes de couleurs
- **Documentation** : Commenter les modifications importantes

### Tests Recommandés
- Test cross-browser (Chrome, Firefox, Safari, Edge)
- Validation W3C CSS
- Test des animations sur différents appareils
- Vérification des chemins de ressources