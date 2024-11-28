# Programme de Gestion de Tournoi

## Description
Ce projet est une application Python de gestion de tournoi, conçue pour organiser et suivre les compétitions. Le programme facilite la création de tournois, l’ajout de joueurs, le suivi des matchs et des scores, ainsi que la génération de classements. 

Le programme est simple et adaptable, offrant des options pour démarrer un tournoi, gérer les tours et afficher les résultats de manière conviviale grâce à des affichages esthétiques dans le terminal, réalisés avec la bibliothèque `Rich`.

# Installation

## Prérequis
- Python 3.x
```
https://www.python.org/
```
- Git  
```
https://git-scm.com/
```

## Étapes d'Installation
1. **Clonez le dépôt du projet**  
- Ouvrez un terminal/invite de commande, puis exécutez la commande suivante :
   ```
   git clone https://github.com/Nono3428/Projet4_OC.git
   ```
- Placez-vous dans le dossier
    ```
    cd .\Projet4_OC
    ```
- Créez un environnement virtuel :
    ```
    python -m venv env
    ```
    Activez l'environnement virtuel :
    ```
    env\Scripts\activate
    ```
- Installez les dépendances :
    ```
    pip install -r requirements.txt
    ```
- Génération du rapport pour flake8 avec la commande :
    ```
    flake8 .\src\ --format=html --htmldir=flake8_rapport
    ```
- Utilisation :
Lancer l'application : Dans le terminal, lancez le programme principal pour accéder au menu et commencer à utiliser l'application.
    ```
    python main.py
    ```
- Menu Principal : Depuis le menu principal, vous pouvez naviguer entre les différentes options pour ajouter des joueurs, créer des tournois, gérer les tours et afficher les classements.

- Gestion du Tournoi :

    - Ajouter des Joueurs : Ajoutez des joueurs en spécifiant leurs informations.
    - Afficher les Détails : Consultez les informations spécifiques à chaque tournoi.
    - Démarrer le Tournoi : Lancez le tournoi, gérez les tours et enregistrez les scores des matchs.
    - Afficher le Classement : Consultez le classement en fonction des scores mis à jour.

Exemples de Commandes :
Créer un joueur
Accédez à l'option "Ajouter joueur" dans le menu principal, puis entrez les informations requises pour chaque joueur (nom, prénom, identifiant, etc.).

Créer un tournoi
Sélectionnez "Créer un nouveau tournoi" depuis le menu principal et suivez les instructions pour définir les détails du tournoi (nom, lieu, dates, etc.).

- Désactivez l'environnement virtuel :
    ```
    env\Scripts\deactivate
    ```