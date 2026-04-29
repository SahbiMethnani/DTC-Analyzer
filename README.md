# 🚗 DTC Analyzer — WPM XCT

> Plateforme de visualisation, d'analyse et de gestion des **Codes Défauts (DTC)** issus de fichiers d'acquisition véhicule, développée avec Streamlit et MySQL.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square&logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?style=flat-square&logo=mysql)
![CI](https://github.com/SahbiMethnani/DTC-Analyzer/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📖 Description

**DTC Analyzer** est un outil interne développé dans le cadre du projet **WPM XCT** pour centraliser et exploiter les données de diagnostic véhicule. Il permet d'ingérer des fichiers d'acquisition MDF, d'en extraire les codes défauts (DTC), de les stocker en base de données MySQL et de les visualiser à travers un dashboard interactif.

L'application couvre l'ensemble de la chaîne :

- **Acquisition** — parsing des fichiers MDF et insertion en base
- **Analyse** — visualisation par calculateur, type, kilométrage et période
- **Suivi** — évolution temporelle, vue hebdomadaire, statut de traitement
- **Exploitation** — import/export Excel et PDF, lancement des jobs de traitement
- **Administration** — gestion de la configuration et des exécutables via une interface sécurisée

---

## ✨ Fonctionnalités

| Page | Description |
|------|-------------|
| 📊 **Vue globale** | KPIs généraux, répartition par calculateur, top 15 DTC, analyse par kilométrage |
| 📁 **Fichiers & DTC** | Navigation par fichier d'acquisition, détail complet des DTC associés |
| 📈 **Évolution temporelle** | Courbes jour / semaine / mois, sous-graphes par type DTC (P / C / B / U) |
| 📅 **Vue hebdomadaire** | Heatmap semaine × jour, classement des semaines les plus chargées |
| 📥 **Import Excel** | Insertion en base depuis un fichier `.xlsx` avec validation des colonnes |
| 📤 **Export** | Export des données filtrées en Excel ou PDF |
| ⚙️ **Contrôle** | Interface d'administration sécurisée (voir section dédiée) |

---

## 🏗️ Architecture du projet

```
DTC-Analyzer/
│
├── app.py                        # Point d'entrée + routage des pages
├── config.py                     # Chargement centralisé des variables d'environnement
├── requirements.txt              # Dépendances Python
├── .env.example                  # Modèle de configuration (à copier en .env)
│
├── database/
│   ├── connection.py             # Pool de connexions MySQL + helpers query / execute
│   └── loaders.py                # Chargeurs de données avec mise en cache (@st.cache_data)
│
├── views/                        # Pages de l'application
│   ├── vue_globale.py
│   ├── fichiers_dtc.py
│   ├── evolution_temporelle.py
│   ├── vue_hebdomadaire.py
│   ├── import_excel.py
│   ├── export.py
│   └── controle.py               # Page d'administration sécurisée
│
├── components/
│   ├── charts.py                 # Graphiques Plotly réutilisables
│   ├── metrics.py                # Composant carte métrique
│   └── sidebar.py                # Barre latérale + filtres globaux
│
├── utils/
│   ├── style.py                  # CSS global, palette de couleurs, thème Plotly
│   ├── filters.py                # Logique de filtrage des DataFrames
│   └── export_helpers.py         # Génération des fichiers Excel et PDF
│
├── tests/
│   └── test_utils.py             # Tests unitaires
│
└── .github/
    └── workflows/
        └── ci.yml                # Pipeline CI GitHub Actions
```

> ⚠️ Le dossier est nommé `views/` et non `pages/` pour éviter le routing automatique de Streamlit qui génère une navigation dupliquée.

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- MySQL 8.0+
- Git

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/SahbiMethnani/DTC-Analyzer.git
cd DTC-Analyzer

# 2. Créer un environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Lancer l'application
streamlit run app.py
```

---

## ⚙️ Configuration (.env)

Copiez `.env.example` en `.env` et renseignez vos valeurs :

```env
# Base de données
DB_HOST=localhost
DB_NAME=dtc_db
DB_USER=root
DB_PASSWORD=
DB_PORT=3306
DB_POOL_SIZE=5

# Chemins des jobs
JOB1_PATH=jobs/job1.exe
JOB1_LABEL=Job 1 - Acquisition
JOB2_PATH=jobs/job2.exe
JOB2_LABEL=Job 2 - Traitement

# Application
APP_TITLE=DTC Analyzer
APP_DEBUG=false
```

| Variable        | Description                            | Défaut          |
|-----------------|----------------------------------------|-----------------|
| `DB_HOST`       | Hôte du serveur MySQL                  | `localhost`     |
| `DB_NAME`       | Nom de la base de données              | `dtc_db`        |
| `DB_USER`       | Utilisateur MySQL                      | `root`          |
| `DB_PASSWORD`   | Mot de passe MySQL                     | _(vide)_        |
| `DB_PORT`       | Port MySQL                             | `3306`          |
| `DB_POOL_SIZE`  | Nombre de connexions dans le pool      | `5`             |
| `JOB1_PATH`     | Chemin vers l'exécutable du job 1      | `jobs/job1.exe` |
| `JOB1_LABEL`    | Libellé affiché pour le job 1          | —               |
| `JOB2_PATH`     | Chemin vers l'exécutable du job 2      | `jobs/job2.exe` |
| `JOB2_LABEL`    | Libellé affiché pour le job 2          | —               |
| `APP_TITLE`     | Titre affiché dans l'onglet navigateur | `DTC Analyzer`  |
| `APP_DEBUG`     | Active les logs de debug               | `false`         |

> ⚠️ **Ne committez jamais votre fichier `.env`** — il est exclu par le `.gitignore`.

---

## 🔒 Page Contrôle

La page **⚙️ Contrôle** est accessible depuis la sidebar via une authentification par mot de passe.

Elle offre deux onglets :

### ▶ Exécution des Jobs

Permet de lancer les exécutables de traitement directement depuis l'interface :

- Lancement asynchrone de `job1.exe` et `job2.exe`
- Badge d'état en temps réel : **Inactif / En cours / Succès / Erreur**
- Affichage de la sortie console (`stdout` en vert, `stderr` en rouge)
- Bouton de réinitialisation après chaque exécution

### 🛠 Variables d'environnement

Permet de modifier la configuration sans toucher aux fichiers manuellement :

- Formulaire d'édition groupé par catégorie (DB, Jobs, Application)
- Sauvegarde directe dans le fichier `.env` avec préservation des commentaires
- Aperçu du contenu du `.env` avec les mots de passe masqués automatiquement

---

## 🗄️ Structure de la base de données

```sql
-- Fichiers d'acquisition
CREATE TABLE t_acq_files (
    id             INT PRIMARY KEY AUTO_INCREMENT,
    path           VARCHAR(500),
    moyen          VARCHAR(100),
    datecreated    VARCHAR(50),
    dateprocessed  VARCHAR(50),
    nbdefaut       INT,
    invalid        TINYINT DEFAULT 0
);

-- Codes défauts
CREATE TABLE t_dtc (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    date                VARCHAR(50),
    DTC                 VARCHAR(20),
    calculateur         VARCHAR(50),
    Kilometrage         INT,
    delai_apparition    FLOAT,
    groupe_apparition   VARCHAR(100),
    status_suivi        VARCHAR(100),
    commentaire         TEXT,
    id_t_acq_files      INT,
    Channel             INT,
    FOREIGN KEY (id_t_acq_files) REFERENCES t_acq_files(id),
    FOREIGN KEY (Channel) REFERENCES t_channel(id)
);

-- Canaux
CREATE TABLE t_channel (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    L_CHANNELS  VARCHAR(200)
);
```

---

## 📦 Dépendances

| Package                    | Version    | Usage                          |
|----------------------------|------------|--------------------------------|
| `streamlit`                | ≥ 1.35     | Framework UI                   |
| `pandas`                   | ≥ 2.0      | Manipulation des données       |
| `plotly`                   | ≥ 5.20     | Graphiques interactifs         |
| `mysql-connector-python`   | ≥ 8.3      | Connexion MySQL                |
| `openpyxl`                 | ≥ 3.1      | Import / Export Excel          |
| `python-dotenv`            | ≥ 1.0      | Chargement du `.env`           |
| `fpdf2`                    | ≥ 2.7      | Génération de PDF              |

---

## 🧪 Tests & CI

Le projet utilise **GitHub Actions** pour l'intégration continue.

À chaque push sur `main` :
1. Installation des dépendances
2. Lint avec `flake8` (erreurs bloquantes + style)
3. Tests unitaires avec `pytest`

Pour lancer les tests en local :

```bash
pytest tests/ -v
```

---

## 🛠 Étendre l'application

### Ajouter une nouvelle page

1. Créer `views/ma_page.py` avec une fonction `render(...)`
2. Ajouter l'entrée dans `PAGES` dans `components/sidebar.py`
3. Ajouter le routage dans `app.py`

### Modifier le thème

Tout est centralisé dans `utils/style.py` :

- `COLORS` — palette principale
- `CALC_COLORS` — couleurs par calculateur (ECU, TCU, BCM, CCM, CGW, VCU)
- `TYPE_COLORS` — couleurs par type DTC (P, C, B, U)
- `PLOTLY_THEME` — thème appliqué à tous les graphiques Plotly

---

## 📄 Licence

MIT — libre d'utilisation, de modification et de distribution.