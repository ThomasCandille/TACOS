# Documentation - index.html

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
**Position :** Point d'entrée principal de l'application TACOS  
**Rôle :** Interface de connexion permettant l'authentification utilisateur avant l'accès aux fonctionnalités de génération de fiches de coordination

### Description
Le fichier [`index.html`](../../web/index.html) constitue la page d'accueil et d'authentification de l'application TACOS. Il fournit une interface de connexion sécurisée utilisant les identifiants NNI et mot de passe pour l'accès aux données de la base ANIS et aux fonctionnalités de génération de fiches Excel.

## Fonctionnalités Principales

### Interface de Connexion
- **Formulaire d'authentification** : Champs NNI et mot de passe avec validation
- **Design corporatif RTE** : Interface alignée avec l'identité visuelle
- **Gestion d'erreurs** : Affichage des erreurs d'authentification

```html
<form action="" id="connexion_form">
  <h1 class="element_connexion">Connexion</h1>
  
  <div class="solo_input element_connexion">
    <input type="text" id="nni" placeholder="NNI" required />
  </div>
  
  <div class="solo_input element_connexion">
    <input type="password" id="password" placeholder="Mot de passe" required />
  </div>
  
  <div class="container_button">
    <button id="getdata" class="button_input">Se connecter</button>
  </div>
</form>
```

### Éléments Visuels
- **Logo RTE** : Affichage du logotype externe RTE en en-tête
- **Image de fond** : Thématique éolienne pour le contexte énergétique
- **Layout responsive** : Interface adaptée aux dimensions d'application desktop

### Navigation Post-Authentification
- **Redirection automatique** : Vers [`filters.html`](../../web/pages/filters.html) après connexion réussie
- **Feedback utilisateur** : Messages d'erreur via alertes JavaScript

## Dépendances & Imports

### Ressources Externes
```html
<!-- Framework de communication Python-JavaScript -->
<script type="text/javascript" src="../eel.js"></script>

<!-- Styles personnalisés -->
<link rel="stylesheet" href="css/style.css" />

<!-- Script de gestion de connexion -->
<script src="js/script.js"></script>

<!-- Favicon -->
<link rel="icon" href="img/RTE_Logotype_interne_RVB_Bleu.svg" />

<!-- Logo corporatif -->
<img src="./img/RTE_Logotype_externe_RVB_Bleu.png" alt="logo" />
```

### Dépendances du Projet
- **[style.css](../../web/css/style.css)** : Feuille de style principale avec styles spécialisés pour la connexion
- **[script.js](../../web/js/script.js)** : Logique de connexion et communication backend
- **eel.js** : Bridge de communication avec le backend Python
- **Assets RTE** : Logos et images d'identité visuelle

### Intégration Backend
- **[script.py](../../script.py)** : Serveur Python avec fonctions d'authentification exposées
- **API ANIS** : Système d'authentification RTE via [`query_utils.py`](../../query_utils.py)
- **Session Management** : Gestion des tokens d'authentification

## Structure du Code

### Architecture HTML5 Sémantique
```html
<div class="container_all" id="connexion_page">
  <header>
    <!-- Logo RTE -->
    <img class="header-logo" src="./img/RTE_Logotype_externe_RVB_Bleu.png" alt="logo" />
  </header>
  
  <form action="" id="connexion_form">
    <!-- Titre et champs de connexion -->
    <h1 class="element_connexion">Connexion</h1>
    <div class="solo_input element_connexion">...</div>
    <div class="container_button">...</div>
  </form>
  
  <footer></footer>
</div>
```

### Flux d'Authentification
1. **Chargement initial** : Affichage du formulaire de connexion
2. **Saisie utilisateur** : NNI et mot de passe avec validation HTML5
3. **Soumission** : Appel JavaScript vers [`script.js`](../../web/js/script.js)
4. **Validation backend** : Communication Eel vers [`script.py`](../../script.py)
5. **Réponse** : Redirection ou affichage d'erreur

### Mécanismes de Validation
```html
<!-- Validation HTML5 native -->
<input type="text" id="nni" placeholder="NNI" required />
<input type="password" id="password" placeholder="Mot de passe" required />
```

### Gestion d'État
- **État initial** : Formulaire vide avec focus sur NNI
- **État de soumission** : Désactivation du bouton pendant traitement
- **État d'erreur** : Affichage d'alertes avec messages spécifiques
- **État de succès** : Redirection vers interface principale

## Exemples d'Utilisation

### Workflow Standard Utilisateur
```javascript
// 1. Utilisateur remplit le formulaire
document.getElementById('nni').value = "123456";
document.getElementById('password').value = "motdepasse";

// 2. Clic sur "Se connecter" déclenche script.js
document.getElementById('getdata').onclick = () => {
  const form_data = {
    'nni': document.getElementById("nni").value,
    'mdp': document.getElementById("password").value
  };
  
  // 3. Appel vers backend Python
  eel.get_data(form_data['nni'], form_data['mdp']);
};
```

### Intégration avec Backend
```python
# Dans script.py - Fonction d'authentification
@eel.expose
def get_data(nni, mdp):
    global headers
    headers, response_tuple = get_headers(nni, mdp)
    if (headers is None):
        # Échec d'authentification
        eel.display_error(response_tuple)
    else:
        # Succès - redirection
        eel.go_to('./pages/filters.html')
```

### Cas d'Usage Typiques
```javascript
// Gestion des erreurs côté client
eel.expose(display_error);
function display_error(response_tuple) {
  alert(`Error ${response_tuple[0]} - ${response_tuple[1]}`);
}

// Navigation post-authentification
eel.expose(go_to);
function go_to(url) {
  window.location.replace(url);
}
```

## Configuration & Paramètres

### Paramètres d'Interface
- **Titre de page** : `"Fiche de Coordination"`
- **Placeholders** : 
  - `"NNI"` pour l'identifiant
  - `"Mot de passe"` pour le champ password
- **Label bouton** : `"Se connecter"`

### Identifiants JavaScript Configurables
```javascript
// Éléments du formulaire
"nni"              // Champ identifiant utilisateur
"password"         // Champ mot de passe
"getdata"          // Bouton de soumission
"connexion_form"   // Formulaire principal
"connexion_page"   // Container principal
```

### Classes CSS Spécialisées
```css
.container_all         /* Container principal application */
#connexion_page        /* Page de connexion avec fond éolienne */
#connexion_form        /* Formulaire avec ombre et bordure */
.element_connexion     /* Éléments avec padding uniforme */
.solo_input           /* Container champs de saisie */
.container_button     /* Container bouton centré */
.header-logo          /* Style logo RTE */
```

### Tailles et Dimensions
```javascript
// Dans script.js - Configuration fenêtre
window.resizeTo(500, 300); // Dimensions application desktop
```

## Notes Techniques

### Considérations de Sécurité
- **Type password** : Masquage automatique du mot de passe
- **Validation required** : Contrôles HTML5 côté client
- **Communication sécurisée** : Token d'authentification via API ANIS
- **Session temporaire** : Pas de persistance locale des identifiants

### Optimisations de Performance
```html
<!-- Ressources optimisées -->
<link rel="icon" href="img/RTE_Logotype_interne_RVB_Bleu.svg" /> <!-- SVG pour favicon -->
<img src="./img/RTE_Logotype_externe_RVB_Bleu.png" alt="logo" /> <!-- PNG pour qualité -->
```

### Patterns d'Architecture
- **Progressive Enhancement** : Fonctionnalité de base HTML + amélioration JavaScript
- **Separation of Concerns** : Structure HTML, présentation CSS, comportement JavaScript
- **Event-Driven** : Réactivité basée sur les événements utilisateur
- **Single Responsibility** : Page dédiée uniquement à l'authentification

### Gestion d'Erreurs Robuste
```javascript
// Dans script.js - Gestion centralisée des erreurs
eel.expose(display_error);
function display_error(response_tuple) {
  alert(`Error ${response_tuple[0]} - ${response_tuple[1]}`);
}
```

### Compatibilité et Standards
- **HTML5 Semantic** : Utilisation des éléments sémantiques appropriés
- **CSS Grid/Flexbox** : Layout moderne et responsive
- **ES6+ JavaScript** : Syntaxe moderne pour les event handlers
- **Accessibilité** : Labels implicites et navigation clavier

## Maintenance & Développement

### Modifications Courantes
```html
<!-- Ajout de champs supplémentaires -->
<div class="solo_input element_connexion">
  <input type="text" id="nouveau_champ" placeholder="Nouveau Champ" required />
</div>
```

### Extension JavaScript
```javascript
// Dans script.js - Extension pour nouveaux champs
document.getElementById('getdata').onclick = () => {
  const form_data = {
    'nni': document.getElementById("nni").value,
    'mdp': document.getElementById("password").value,
    'nouveau_champ': document.getElementById("nouveau_champ").value // Ajout
  };
  
  eel.get_data(form_data['nni'], form_data['mdp'], form_data['nouveau_champ']);
};
```

### Personnalisation Visuelle
```css
/* Modification du thème dans style.css */
#connexion_page {
  background-image: url("../img/nouveau_fond.png"); /* Nouveau fond */
}

.header-logo {
  height: 150%; /* Ajustement taille logo */
}
```

### Tests et Debugging
- **Console Browser** : Monitoring des appels Eel et gestion d'erreurs
- **Network Tab** : Vérification des requêtes d'authentification
- **Application Tab** : Vérification absence stockage sensible
- **Lighthouse** : Audit performance et accessibilité

### Guidelines de Contribution
1. **Sécurité** : Ne jamais stocker d'identifiants en local
2. **UX** : Maintenir le feedback utilisateur clair et immédiat
3. **Branding** : Respecter l'identité visuelle RTE
4. **Performance** : Optimiser les assets (images, fonts)
5. **Accessibilité** : Conserver les attributs `alt`, `required`, et la navigation clavier

### Fichiers Associés à Modifier
- **[script.js](../../web/js/script.js)** : Logique d'authentification et navigation
- **[script.py](../../script.py)** : Fonction backend `get_data()` pour nouveaux paramètres
- **[style.css](../../web/css/style.css)** : Styles pour nouveaux éléments d'interface
- **[query_utils.py](../../query_utils.py)** : Fonctions d'authentification si modifications nécessaires

### Procédures de Débogage
```javascript
// Debug des données de formulaire
console.log('Données soumises:', {
  nni: document.getElementById("nni").value,
  mdp: document.getElementById("password").value
});

// Debug de la communication Eel
eel.get_data(nni, mdp)._Promise
  .then(result => console.log('Authentification réussie'))
  .catch(error => console.error('Erreur authentification:', error));

// Debug de la navigation
eel.go_to(url)._Promise
  .then(() => console.log('Redirection vers:', url));
```

### Maintenance de Sécurité
1. **Audit régulier** : Vérification des tokens et sessions
2. **Validation backend** : Toujours valider côté serveur
3. **Logs d'accès** : Traçabilité des tentatives de connexion
4. **Rotation des secrets** : Mise à jour périodique des clés API
5. **Tests de pénétration** : Validation de la robustesse d'authentification 