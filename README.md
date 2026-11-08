# DTC Analyzer

Plateforme de visualisation, d’analyse et de gestion des codes défauts (DTC) issus de fichiers d’acquisition véhicule. L’application repose sur Streamlit et MySQL et centralise les opérations d’importation, de traitement, d’analyse et d’exportation des données de diagnostic.

## Présentation

DTC Analyzer est un outil conçu pour centraliser et exploiter les données de diagnostic véhicule. Il permet d’importer des fichiers d’acquisition au format MDF, d’en extraire les codes défauts (DTC), de stocker les informations dans une base de données MySQL et de les consulter au moyen d’un tableau de bord interactif.

L’application couvre l’ensemble du processus de traitement des données :

- **Acquisition :** analyse des fichiers MDF et insertion des données en base.
- **Analyse :** exploration des défauts par calculateur, type, kilométrage et période.
- **Suivi :** consultation de l’évolution temporelle, des statistiques hebdomadaires et du statut de traitement.
- **Exploitation :** importation et exportation de données Excel et PDF, ainsi que lancement des traitements.
- **Administration :** gestion de la configuration et exécution des programmes de traitement depuis une interface protégée.

## Technologies

| Technologie | Version minimale | Rôle |
|---|---:|---|
| Python | 3.10+ | Langage principal |
| Streamlit | 1.35+ | Interface web |
| MySQL | 8.0+ | Stockage des données |
| Pandas | 2.0+ | Manipulation des données |
| Plotly | 5.20+ | Visualisations interactives |
| mysql-connector-python | 8.3+ | Connexion à MySQL |
| OpenPyXL | 3.1+ | Lecture et écriture des fichiers Excel |
| python-dotenv | 1.0+ | Gestion des variables d’environnement |
| fpdf2 | 2.7+ | Génération des rapports PDF |

## Fonctionnalités

| Module | Description |
|---|---|
| Vue globale | Présentation des indicateurs clés, répartition des défauts par calculateur, principaux DTC et analyse par kilométrage. |
| Fichiers et DTC | Consultation des fichiers d’acquisition et affichage des codes défauts associés à chaque fichier. |
| Évolution temporelle | Analyse des défauts par jour, semaine ou mois, avec une distinction par type de DTC (P, C, B et U). |
| Vue hebdomadaire | Visualisation sous forme de heatmap croisant les semaines et les jours, avec classement des périodes les plus chargées. |
| Import Excel | Importation de données depuis des fichiers `.xlsx`, avec validation des colonnes attendues. |
| Export | Exportation des données filtrées aux formats Excel et PDF. |
| Contrôle | Interface d’administration permettant de lancer les traitements et de gérer certains paramètres de configuration. |


## Administration et contrôle des traitements

La page `Contrôle`, accessible depuis la barre latérale, est protégée par une authentification par mot de passe. Elle regroupe deux espaces fonctionnels.

### Exécution des traitements

Cette section permet de lancer les exécutables de traitement depuis l’interface :

- Démarrage asynchrone de `job1.exe` et `job2.exe`.


## Tests et intégration continue

Le projet utilise GitHub Actions pour exécuter un pipeline d’intégration continue.

À chaque `push` sur la branche `main`, le pipeline effectue les opérations suivantes :

1. Installation des dépendances.
2. Analyse statique du code avec `flake8`.
3. Exécution des tests unitaires avec `pytest`.
