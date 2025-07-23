# Script.js - Documentation

## Table des Matières
1. [Aperçu du Fichier](#aperçu-du-fichier)
2. [Fonctionnalités Principales](#fonctionnalités-principales)
3. [Dépendances & Imports](#dépendances--imports)
4. [Structure du Code](#structure-du-code)
5. [Exemples d'Utilisation](#exemples-dutilisation)
6. [Configuration & Paramètres](#configuration--paramètres)
7. [Notes Techniques](#notes-techniques)
8. [Maintenance & Développement](#maintenance--développement)

## Aperçu du Fichier

**Type de fichier** : JavaScript client-side  
**Technologie** : JavaScript ES5/ES6 avec intégration Eel (Python-JavaScript Bridge)  
**Position dans l'architecture** : Module de gestion de l'interface de connexion côté frontend  

Ce fichier constitue le point d'entrée principal de l'interface utilisateur pour l'application TACOS. Il gère spécifiquement la page de connexion et établit la communication bidirectionnelle entre l'interface web et le backend Python via la bibliothèque Eel.

**Rôle principal** : Orchestrer l'authentification utilisateur et la navigation vers les pages suivantes de l'application.

## Fonctionnalités Principales

### 1. Configuration de la Fenêtre
```javascript
window.resizeTo(500, 300)
```
- Définit automatiquement la taille de la fenêtre à 500x300 pixels
- Optimise l'affichage pour une interface de connexion compacte

### 2. Interface Eel (Python-JavaScript Bridge)

#### Fonctions Exposées au Backend Python
```javascript
eel.expose(go_to)
function go_to(url){window.location.replace(url)}
```
- **`go_to(url)`** : Fonction de navigation exposée à Python pour rediriger vers une nouvelle page
- Utilise `window.location.replace()` pour éviter l'historique de navigation

```javascript
eel.expose(display_error)
function display_error(response_tuple){
  alert(`Error ${response_tuple[0]} - ${response_tuple[1]}`)
}
```
- **`display_error(response_tuple)`** : Affiche les erreurs de connexion renvoyées par le backend
- Attend un tuple `[code_erreur, message_erreur]`
- Utilise une alerte JavaScript native pour l'affichage

### 3. Gestion de l'Authentification
```javascript
document.getElementById('getdata').onclick = () => {
  const form_data = {
    'nni': document.getElementById("nni").value,
    'mdp': document.getElementById("password").value
  };
eel.get_data(form_data['nni'], form_data['mdp'])
};
```
- **Capture des données** : Récupère les valeurs des champs NNI et mot de passe
- **Validation côté client** : Collecte les informations d'identification
- **Communication backend** : Transmet les données au script Python via `eel.get_data()`

## Dépendances & Imports

### Dépendances Externes
- **Eel Framework** : Chargé via `<script type="text/javascript" src="../eel.js"></script>`
  - Bibliothèque Python-JavaScript pour la communication bidirectionnelle
  - Permet l'exécution de fonctions Python depuis JavaScript et vice versa

### Dépendances Internes
- **HTML Elements** : Référence les éléments du DOM de la page index.html
  - `#nni` : Champ de saisie NNI
  - `#password` : Champ de saisie mot de passe
  - `#getdata` : Bouton de soumission

### Environnement Requis
- Navigateur web moderne supportant ES6+
- Runtime Eel actif (serveur Python en arrière-plan)
- Accès DOM complet

## Structure du Code

### 1. Initialisation de l'Interface
```
Configuration fenêtre → Exposition des fonctions → Gestion des événements
```

### 2. Flux d'Exécution Principal
1. **Chargement de la page** → Redimensionnement automatique de la fenêtre
2. **Exposition des fonctions** → Enregistrement des callbacks pour Python
3. **Interaction utilisateur** → Capture des événements de clic
4. **Communication backend** → Transmission des données via Eel
5. **Gestion des réponses** → Navigation ou affichage d'erreurs

### 3. Modèles de Conception Utilisés
- **Observer Pattern** : Écoute des événements DOM (`onclick`)
- **Bridge Pattern** : Communication JavaScript-Python via Eel
- **Facade Pattern** : Simplification de l'interface de navigation

### 4. Mécanismes de Gestion d'Erreurs
- **Gestion centralisée** : La fonction `display_error()` centralise l'affichage des erreurs
- **Validation backend** : Les erreurs de connexion sont gérées côté Python et renvoyées pour affichage
- **Interface utilisateur** : Utilisation d'alertes natives pour un feedback immédiat

## Exemples d'Utilisation

### 1. Intégration dans une Page HTML
```html
<script type="text/javascript" src="../eel.js"></script>
<script src="js/script.js"></script>
```

### 2. Appel depuis Python (Backend)
```python
# Redirection après connexion réussie
eel.go_to('./pages/filters.html')

# Affichage d'erreur de connexion
eel.display_error((401, "Identifiants incorrects"))
```

### 3. Structure de Données Attendues
```javascript
// Format du tuple d'erreur
response_tuple = [error_code, error_message]
// Exemple : [401, "Unauthorized access"]
```

### 4. Interaction Utilisateur Typique
1. L'utilisateur saisit son NNI et mot de passe
2. Clic sur le bouton "Se connecter"
3. Transmission des données au backend Python
4. Redirection vers `/pages/filters.html` en cas de succès
5. Affichage d'une alerte en cas d'erreur

## Configuration & Paramètres

### Paramètres de Fenêtre
- **Largeur** : 500 pixels (fixe)
- **Hauteur** : 300 pixels (fixe)
- **Redimensionnement** : Automatique au chargement

### Éléments DOM Requis
- `#nni` : Champ de saisie NNI
- `#password` : Champ de saisie mot de passe
- `#getdata` : Bouton de soumission

### Variables d'Environnement
- Aucune variable d'environnement directe
- Dépend de la configuration Eel côté Python

## Notes Techniques

### Considérations de Performance
- **Chargement synchrone** : Le script attend le chargement complet du DOM
- **Communication asynchrone** : Les appels Eel sont non-bloquants
- **Gestion mémoire** : Utilisation de `window.location.replace()` pour éviter l'accumulation d'historique

### Mesures de Sécurité
- **Validation côté serveur** : La validation des identifiants est déléguée au backend Python
- **Pas de stockage local** : Les identifiants ne sont pas persistés côté client
- **Communication sécurisée** : Transit via le bridge Eel (localhost)

### Limitations Connues
- **Dépendance Eel** : L'application ne fonctionne que si le serveur Python Eel est actif
- **Validation limitée** : Aucune validation côté client des formats de données

### Compatibilité
- **Navigateurs** : Chrome, Firefox, Safari (versions récentes)
- **Systèmes** : Compatible plateforme Windows
- **JavaScript** : ES5+ requis pour les arrow functions

## Maintenance & Développement

### Instructions de Modification

#### Ajout de Nouvelles Validations
```javascript
// Exemple d'ajout de validation NNI
document.getElementById('getdata').onclick = () => {
  const nni = document.getElementById("nni").value;
  const password = document.getElementById("password").value;
  
  // Nouvelle validation
  if (!nni || nni.length < 6) {
    alert("NNI invalide");
    return;
  }
  
  eel.get_data(nni, password);
};
```

#### Extension des Fonctions Exposées
```javascript
// Nouvelle fonction exposée pour Python
eel.expose(new_function)
function new_function(data) {
  // Implementation
}
```

### Tests Recommandés
1. **Test d'intégration** : Vérifier la communication Eel
2. **Test d'interface** : Validation des éléments DOM
3. **Test de navigation** : Contrôler les redirections
4. **Test d'erreurs** : Simuler les échecs de connexion

### Débogage
```javascript
// Ajouter des logs pour le débogage
console.log("Form data:", form_data);
console.log("Eel call initiated");
```

### Guidelines de Contribution
- Maintenir la compatibilité Eel
- Préserver la structure des fonctions exposées
- Documenter les nouveaux paramètres de configuration
- Respecter le pattern de gestion d'erreurs existant

### Points d'Extension Futurs
- Validation côté client avancée
- Gestion de session
- Support multilingue