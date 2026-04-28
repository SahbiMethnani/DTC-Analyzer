# DTC Dashboard — WPM XCT

Dashboard Streamlit pour la visualisation et la gestion des codes défauts (DTC).

---

## 📁 Structure du projet

```
dtc_dashboard/
│
├── app.py                        # Point d'entrée (routing des pages)
├── config.py                     # Chargement de la config depuis .env
├── requirements.txt              # Dépendances Python
├── .env.example                  # Modèle de variables d'environnement
├── .env                          # Variables d'environnement (à créer, non versionné)
│
├── database/
│   ├── __init__.py
│   ├── connection.py             # Pool MySQL + helpers query/execute
│   └── loaders.py                # Loaders avec cache Streamlit (@cache_data)
│
├── pages/
│   ├── __init__.py
│   ├── vue_globale.py            # Page Vue globale (KPIs, charts)
│   ├── fichiers_dtc.py           # Page Fichiers & DTC
│   ├── evolution_temporelle.py   # Page Évolution temporelle
│   ├── vue_hebdomadaire.py       # Page Vue hebdomadaire
│   ├── import_excel.py           # Page Import Excel → DB
│   ├── export.py                 # Page Export Excel/PDF
│   └── controle.py               # Page Contrôle (protégée par MDP)
│
├── components/
│   ├── __init__.py
│   ├── charts.py                 # Helpers Plotly réutilisables
│   ├── metrics.py                # Composant metric_card
│   └── sidebar.py                # Sidebar + filtres globaux
│
├── utils/
│   ├── __init__.py
│   ├── style.py                  # CSS, thème Plotly, couleurs
│   ├── filters.py                # Application des filtres DataFrames
│   └── export_helpers.py         # Export Excel & PDF
│
└── jobs/
    ├── job1.exe                  # Job 1 (à placer ici ou configurer via .env)
    └── job2.exe                  # Job 2 (à placer ici ou configurer via .env)
```

---

## 🚀 Installation

```bash
# 1. Cloner / copier le projet
cd dtc_dashboard

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Lancer le dashboard
streamlit run app.py
```

---

## ⚙️ Variables d'environnement (.env)

| Variable          | Description                        | Défaut         |
|-------------------|------------------------------------|----------------|
| `DB_HOST`         | Hôte MySQL                         | `localhost`    |
| `DB_NAME`         | Nom de la base de données          | `dtc_db`       |
| `DB_USER`         | Utilisateur MySQL                  | `root`         |
| `DB_PASSWORD`     | Mot de passe MySQL                 | _(vide)_       |
| `DB_PORT`         | Port MySQL                         | `3306`         |
| `DB_POOL_SIZE`    | Taille du pool de connexions       | `5`            |
| `JOB1_PATH`       | Chemin vers le premier .exe        | `jobs/job1.exe`|
| `JOB1_LABEL`      | Libellé affiché pour le job 1      | `Job 1 — Acquisition` |
| `JOB2_PATH`       | Chemin vers le deuxième .exe       | `jobs/job2.exe`|
| `JOB2_LABEL`      | Libellé affiché pour le job 2      | `Job 2 — Traitement`  |
| `APP_TITLE`       | Titre de l'application             | `DTC Dashboard · WPM XCT` |
| `APP_DEBUG`       | Mode debug                         | `false`        |
| `CONTROL_PASSWORD`| Mot de passe de la page Contrôle  | `admin123`     |

---

## 🔒 Page Contrôle

La page **⚙️ Contrôle** est accessible uniquement via un mot de passe défini
dans la variable `CONTROL_PASSWORD` du fichier `.env`.

Elle permet de :
- **Lancer les jobs** (job1.exe, job2.exe) et voir leur sortie console
- **Éditer les variables** du fichier `.env` sans toucher aux fichiers manuellement
- **Prévisualiser** le contenu du `.env` (mots de passe masqués)

---

## 📦 Ajouter une nouvelle page

1. Créer `pages/ma_page.py` avec une fonction `render(...)`
2. Ajouter l'entrée dans `PAGES` dans `components/sidebar.py`
3. Ajouter le routage dans `app.py`

---

## 🎨 Personnalisation du thème

Toutes les couleurs et le thème Plotly sont centralisés dans `utils/style.py`.
Modifiez `COLORS`, `CALC_COLORS`, `TYPE_COLORS` et `PLOTLY_THEME` pour
adapter l'apparence sans toucher aux pages.
