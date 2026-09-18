# 🇲🇦 Maroc Invest

Plateforme web de présentation des **opportunités d'investissement au Maroc** : site vitrine interactif, tableau de bord socio-économique, flux d'actualités économiques en temps réel et inscription à une newsletter.

> Projet réalisé par **Mouad Bourass**.

---

## 📌 Fonctionnalités

- 🌐 **Site web** : grands projets réalisés, projets en cours (2026), vision 2030-2050, secteurs porteurs, avantages, opportunités d'investissement et carte interactive des régions du Maroc.
- 📊 **Dashboard Streamlit** : indicateurs clés et graphiques interactifs (Plotly) sur la démographie, le PIB, le marché du travail, les finances publiques, l'éducation, l'agriculture et la pêche, le tourisme, l'énergie et les mines, le BTP et l'immobilier, et les indicateurs monétaires.
- 📰 **Actualités économiques** : récupération automatique des flux RSS de Hespress, Médias24 et Le360, exposée via une API.
- 📧 **Newsletter** : formulaire d'inscription (email, téléphone) et script d'envoi aux abonnés.

---

## 🗂️ Structure du projet

```text
MOUAD_BOURASS_PROJET_1/
├── site-web/                  # Front-end (HTML, CSS, JS, Bootstrap 5)
│   ├── index.html             # Page principale (carte, projets, secteurs, actualités…)
│   ├── newsletter.html        # Page d'inscription à la newsletter
│   ├── donnees_maroc.json     # Données utilisées par la carte
│   └── *.png                  # Images et logos
│
├── dashboard/                 # Tableau de bord d'analyse
│   ├── dashboard.py           # Application Streamlit
│   └── donnees_maroc.json     # Données HCP (Haut-Commissariat au Plan)
│
└── FOLDER1/                   # Back-end (Python / FastAPI)
    ├── app.py                 # API newsletter (inscription, statistiques, liste des emails)
    ├── api.py                 # API des actualités (lecture du cache + rafraîchissement)
    ├── scraper.py             # Scraper RSS (Hespress, Médias24, Le360)
    ├── send_newsletter.py     # Script d'envoi de la newsletter
    ├── subscribers.examples.json       # Base des abonnés (fichier JSON)
    └── data/
        └── actualites.json    # Cache des dernières actualités
```

---

## 🛠️ Technologies utilisées

| Partie | Technologies |
|---|---|
| Front-end | HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons |
| Dashboard | Python, Streamlit, Pandas, NumPy, Plotly |
| Back-end | Python, FastAPI, Uvicorn, Pydantic |
| Actualités | feedparser (flux RSS) |
| Données | Fichiers JSON (source : HCP) |

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/MOUAD642207/Projet_HCP_Stage.git


cd MOUAD_BOURASS_PROJET_1
```

### 2. (Optionnel) Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Installer les dépendances

```bash
pip install fastapi uvicorn "pydantic[email]" feedparser requests streamlit pandas numpy plotly
```

---

## ▶️ Lancement

### 🌐 Site web

Ouvrir `site-web/index.html` dans le navigateur, ou lancer un petit serveur local :

```bash
cd site-web
python -m http.server 5500
```

Puis aller sur : http://localhost:5500

### 📊 Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Disponible sur : http://localhost:8501

### 🔌 API Newsletter

```bash
cd FOLDER1
python app.py
```

Disponible sur : http://localhost:8000 (documentation Swagger : http://localhost:8000/docs)

### 📰 API Actualités

Récupérer d'abord les articles :

```bash
cd FOLDER1
python scraper.py
```

Puis lancer l'API :

```bash
uvicorn api:app --port 8000
```

> ⚠️ `app.py` et `api.py` utilisent tous deux le port 8000 : lance-les l'un après l'autre, ou change le port de l'un des deux (et adapte `API_BASE` dans `site-web/index.html`).

### 📧 Envoi de la newsletter

L'API Newsletter (`app.py`) doit être démarrée :

```bash
cd FOLDER1
python send_newsletter.py
```

---

## 🔗 Endpoints de l'API

### Newsletter (`app.py`)

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/` | Page HTML d'inscription |
| `POST` | `/api/subscribe` | Inscrire un abonné (`email`, `phone`, `newsletter`) |
| `GET` | `/api/stats` | Nombre total d'abonnés et d'abonnés newsletter |
| `GET` | `/api/subscribers` | Liste des abonnés |
| `GET` | `/api/newsletter-emails` | Emails des abonnés à la newsletter |

### Actualités (`api.py`)

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/api/actualites` | Retourne les dernières actualités (cache JSON) |
| `POST` | `/api/actualites/refresh` | Relance le scraper et retourne les données à jour |

---

## 📊 Sources des données

- **HCP** : Haut-Commissariat au Plan (Maroc), pour les indicateurs du dashboard.
- **Hespress**, **Médias24**, **Le360** : flux RSS pour les actualités.

---

## 🚀 Améliorations possibles

- Envoi réel des emails (SMTP, SendGrid…) dans `send_newsletter.py`.
- Classification des articles par catégorie (actuellement tous en `macro`).
- Remplacer les fichiers JSON par une vraie base de données (SQLite, PostgreSQL).
- Restreindre les origines CORS en production.
- Déploiement en ligne (Render, Railway, Streamlit Cloud, GitHub Pages).

---

## 👤 Auteur

**Mouad Bourass**
GitHub : [@MOUAD642207](https://github.com/MOUAD642207)
