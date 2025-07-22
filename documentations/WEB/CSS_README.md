# [`web/css/style.css`](web/css/style.css) - Feuille de Style Principale

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
Le fichier [`style.css`](web/css/style.css) constitue la feuille de style principale de l'application TACOS. Il définit l'intégralité de l'apparence visuelle et des interactions utilisateur pour l'interface web du générateur de fiches de coordination.

### Type et Technologie
- **Type** : Feuille de style CSS3
- **Technologie** : CSS (Cascading Style Sheets) avec animations et transformations modernes
- **Position** : Interface utilisateur frontend dans l'architecture [`web/css`](web/css)

### Rôle dans l'Écosystème
Ce fichier centralise toute la stylisation de l'application, implémentant la charte graphique RTE et assurant une expérience utilisateur cohérente à travers toutes les pages de l'interface (index.html, filters.html, OG_choice.html).

## Fonctionnalités Principales

### Reset CSS Complet
Le fichier débute par un reset CSS exhaustif (lignes 8-126) qui normalise l'affichage sur tous les navigateurs :

```css
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
/* ... tous les éléments HTML ... */ {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}
```

### Système de Design RTE
- **Police personnalisée** : Intégration de Nunito depuis les ressources locales
- **Palette de couleurs** : Respect de l'identité visuelle RTE avec bleu principal `#3d70ad`
- **Layout responsive** : Container fixe `375px × 677px` simulant une interface mobile

### Composants Interactifs Avancés

#### Formulaires et Contrôles
```css
.solo_input {
  display: flex;
  flex-direction: column;
  width: 80%;
  height: 12%;
  gap: 2px;
}
```

#### Système de Boutons Hiérarchique
- **Bouton principal** : `#3d70ad` avec états hover et active
- **Bouton secondaire** : `#go_back` avec inversion de couleurs
- **Transitions fluides** : Feedback visuel instantané

### Animation de Chargement Complexe
Implémentation d'un loader animé avec transformations CSS3 avancées (lignes 482-521) :

```css
.loader {
  width: 40px;
  height: 40px;
  mix-blend-mode: darken;
  filter: blur(4px) contrast(10) hue-rotate(270deg);
}

@keyframes l2 {
  12.5% { border-radius: 37% 63% 70% 30% / 30% 62% 38% 70%; }
  25% { border-radius: 84% 16% 15% 85% / 55% 79% 21% 45%; }
  /* ... 8 étapes d'animation morphologique ... */
}
```

## Dépendances & Imports

### Ressources Externes
- **Police Nunito** : `../fonts/NunitoSans-Regular.ttf` (ligne 132)
- **Images de fond** : 
  - `../img/eolienneautre.png` (page de connexion)
  - Logos RTE depuis `../img/`

### Dépendances CSS
- **CSS3 moderne** : Flexbox, Grid, animations, transformations
- **Compatibilité** : Propriétés CSS3 pour navigateurs modernes
- **Fallbacks** : Police de secours `sans-serif`

## Structure du Code

### Organisation Hiérarchique

#### 1. Reset CSS Global (lignes 8-126)
Normalisation complète des styles navigateurs par défaut

#### 2. Configuration des Polices (lignes 128-132)
```css
@font-face {
  font-family: "Nunito";
  src: url("../fonts/NunitoSans-Regular.ttf");
}
```

#### 3. Layout Principal (lignes 134-146)
Conteneur central avec positionnement Flexbox

#### 4. Composants Spécialisés
- **Page de connexion** : `#connexion_page` avec background d'éolienne
- **Formulaires** : Styles pour inputs, selects, radio buttons
- **Listes interactives** : GMR, opérations avec scrolling
- **Système de navigation** : Boutons duo avec hiérarchie visuelle

#### 5. États Interactifs
- **Hover states** : `background-color: #e7edf7`
- **Active states** : `background-color: #274a7d`
- **Focus management** : Accessibilité clavier

#### 6. Utilitaires (lignes 418-425)
```css
.hidden {
  display: none;
  visibility: collapse;
  height: 0;
}
```

## Exemples d'Utilisation

### Intégration dans HTML
```html
<link rel="stylesheet" href="css/style.css">
```

### Application des Classes
```html
<!-- Conteneur principal -->
<div class="container_all">
  <!-- Page de connexion -->
  <div id="connexion_page">
    <!-- Formulaire avec styles -->
    <form id="connexion_form">
      <div class="solo_input">
        <input type="text" placeholder="NNI">
      </div>
    </form>
  </div>
</div>
```

### Boutons Interactifs
```html
<div class="duo_button">
  <button id="go_back">Retour</button>
  <button id="generate_excel">Générer</button>
</div>
```

### Animation de Chargement
```html
<div class="loader"></div>
```

## Configuration & Paramètres

### Variables de Design
- **Couleur principale** : `#3d70ad` (bleu RTE)
- **Couleur secondaire** : `#2f5d9a` (hover)
- **Couleur active** : `#274a7d`
- **Background** : `#eeeeee`
- **Texte** : `#11161a`

### Dimensions du Container
```css
.container_all {
  width: 375px;
  height: 677px;
  background-color: white;
  border-radius: 5px;
}
```

### Espacement et Proportions
- **Gap standard** : `4%`, `24px`
- **Padding formulaire** : `10%` horizontal
- **Border radius** : `5px` (standard), `11px` (formulaires)

## Notes Techniques

### Performance et Optimisations
- **Reset CSS optimisé** : Réduction des recalculs de style
- **Animations CSS pures** : Pas de JavaScript pour les transitions
- **Flexbox moderne** : Layout performant et responsive

### Accessibilité
- **Contrast ratios** : Couleurs conformes aux standards WCAG
- **Focus management** : États visuels pour navigation clavier
- **Police lisible** : Nunito optimisée pour la lisibilité
- **Tailles interactives** : Boutons avec padding suffisant

### Compatibilité Navigateur
- **CSS3 moderne** : Flexbox, animations, transformations
- **Fallbacks** : Police système si Nunito indisponible
- **Propriétés vendor** : Support navigateurs récents

### Limitations Identifiées
- **Dimensions fixes** : Container non responsive (375×677px)
- **Police unique** : Dépendance à Nunito sans variantes
- **Scroll styling** : Style natif pour les listes longues

## Maintenance & Développement

### Modification des Couleurs
Pour adapter la charte graphique, modifier les variables de couleur :
```css
/* Couleur principale RTE */
background-color: #3d70ad; /* → nouvelle couleur */
border: 1px solid #3d70ad; /* → adapter bordures */
```

### Extension des Composants
Ajouter de nouveaux composants en suivant la nomenclature :
```css
.nouveau_composant {
  /* Hériter des patterns existants */
  display: flex;
  flex-direction: column;
  gap: 4%;
}
```

### Débogage des Styles
1. **Vérifier la hiérarchie** : Respect de l'ordre CSS reset → layout → composants
2. **Tester les états** : Hover, active, focus sur tous les éléments interactifs
3. **Valider l'accessibilité** : Contraste et navigation clavier

### Guidelines de Contribution
- **Cohérence** : Suivre les patterns de gap, padding et couleurs existants
- **Performance** : Privilégier CSS pur aux solutions JavaScript
- **Lisibilité** : Commenter les animations complexes et les calculs
- **Tests** : Vérifier sur différentes résolutions et navigateurs

### Structure Recommandée pour Ajouts
```css
/* 1. Nouveau reset si nécessaire */
/* 2. Variables/configuration */
/* 3. Layout principal */
/* 4. Composants spécifiques */
/* 5. États interactifs */
/* 6. Animations */
/* 7. Utilitaires