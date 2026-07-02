# IFRI MentorLink — Rattrapage (2025-2026)

Version simplifiée de MentorLink : une page unique permettant à un mentoré de
rechercher un mentor compatible, sans authentification, selon deux critères :

1. **Au moins une matière/compétence en commun**
2. **Compatibilité horaire avec une tolérance de ± 1 heure**

## Stack

- **Backend** : Django 6 (vues classiques + endpoint JSON, pas besoin de DRF ici)
- **Frontend** : HTML / CSS / JavaScript vanilla (fetch API, une seule page)
- **Base de données** : PostgreSQL (Aiven) en production, SQLite en local

## Structure du projet

```
RPIL_2526_hanto/
├── manage.py
├── mentorlink/          # settings, urls, wsgi du projet
├── matching/             # l'app principale
│   ├── models.py         # Matiere, Mentor, Disponibilite
│   ├── services.py        # le moteur de matching (algorithme)
│   ├── views.py           # page + endpoint JSON /api/rechercher/
│   ├── templates/         # index.html (page unique)
│   ├── static/             # css/js
│   └── management/commands/seed_mentors.py   # pré-remplit 5 mentors de démo
├── requirements.txt
└── .env.example
```

## Installation locale (rapide, avec SQLite)

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_mentors   # crée 5 mentors de démonstration
python manage.py runserver
```

Ouvrez http://127.0.0.1:8000/ — pas besoin de `DATABASE_URL`, le projet
bascule automatiquement sur SQLite s'il n'est pas défini.

## Passer sur PostgreSQL (Aiven) pour la soumission/production

1. Créez un **nouveau service PostgreSQL** sur Aiven (votre instance
   gratuite existante est déjà utilisée par IFRI_MentorLink, il en faut
   une autre — ou un nouveau projet Aiven avec le free tier).
2. Copiez l'URI de connexion (`Service URI` dans la console Aiven).
3. Créez un fichier `.env` à partir de `.env.example` et collez l'URI dans
   `DATABASE_URL` :
   ```
   DATABASE_URL=postgres://avnadmin:xxxxx@xxxxx.aivencloud.com:xxxxx/defaultdb?sslmode=require
   ```
4. Chargez les variables d'environnement (ex: `pip install python-dotenv`
   et `load_dotenv()` en haut de `settings.py`, ou exportez-les manuellement
   dans le terminal) puis relancez :
   ```bash
   python manage.py migrate
   python manage.py seed_mentors
   python manage.py runserver
   ```

> Le `ssl_require=True` est déjà activé dans `settings.py` pour la connexion
> Aiven, aucune config supplémentaire n'est nécessaire côté code.

## Algorithme de matching (`matching/services.py`)

Pour chaque mentor :
- on ignore ceux qui n'ont **aucune matière en commun** avec la recherche ;
- parmi les créneaux restants, on cherche un créneau où l'heure souhaitée
  tombe dans `[heure_debut - 1h, heure_fin + 1h]` ;
- le **score** = jusqu'à 70 points selon la proportion de matières en
  commun + jusqu'à 30 points bonus si la filière correspond (optionnel,
  non éliminatoire) ;
- les résultats sont triés par score décroissant.

## Soumission

```bash
git init
git add .
git commit -m "Rattrapage projet intégrateur - MentorLink simplifié"
git branch -M main
git remote add origin https://github.com/ohinihanto2710-wq/RPIL_2526_hanto.git
git push -u origin main
```

Deadline : **samedi 4 juillet 2026, 15h**.
Présentation en ligne : **lundi 6 juillet 2026, 16h**.
