# Carnet de santé de la femme — application Flask

## Fonctionnalités
- Tableau de bord responsive en français.
- Ajout et suppression d'entrées de vaccination (vaccin, dose, date, rappel, notes).
- Suivi des examens de santé du sein (mammographie, échographie, consultation, IRM, compte rendu résumé et prochaine étape).
- Gestion simple des rendez-vous médicaux.
- Recherche instantanée dans les entrées enregistrées.
- Stockage local dans une base SQLite (`carnet_sante.db`).

## Installation
1. Installer Python 3.10 ou plus récent.
2. Ouvrir un terminal dans le dossier du projet.
3. Installer Flask :
   ```bash
   pip install -r requirements.txt
   ```
4. Démarrer :
   ```bash
   python app.py
   ```
5. Ouvrir http://127.0.0.1:5000 dans le navigateur.

La base SQLite est créée automatiquement au premier lancement.

## Important — confidentialité et santé
Cette version est un prototype local de démonstration, sans authentification ni chiffrement. N'y saisissez pas de vraies données médicales identifiantes avant d'avoir ajouté une authentification robuste, une protection des données, des sauvegardes sécurisées et un hébergement conforme aux règles applicables. Le site sert à organiser les informations et ne donne aucun diagnostic. Les calendriers de vaccination et de dépistage doivent être confirmés par un professionnel de santé selon la situation individuelle et les recommandations locales.
