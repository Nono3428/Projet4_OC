from datetime import datetime
from views.rapport import Rapport
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import rich.box
class Menu:
    def __init__(self):
        self.options = {
            "1": "Ajouter joueur",
            "2": "Liste des joueurs",
            "3": "Créer un nouveau tournoi",
            "4": "Liste des tournois",
            "5": "Sélectionner un tournoi",
            "0": "Quitter"
        }

    def afficher_menu(self):
        console = Console()

        # Titre principal
        titre = Text("Menu Principal", style="bold cyan", justify="center")

        # Création de la table pour les options
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", justify="center", style="yellow")
        table.add_column("Action", style="green")

        # Ajout des options dans la table
        for key, action in self.options.items():
            table.add_row(key, action)

        # Affichage du titre et de la table dans un panneau
        panel = Panel.fit(
            table,
            title = titre,
            border_style = "bright_blue",
            padding=(1, 2)
        )
        console.print(panel)

    def afficher_menu_tournoi(self, tournoi_nom):
        console = Console()

        # Création de la table pour les options avec la bordure correcte
        table = Table(show_header=True, header_style="bold magenta")

        # Ajouter les colonnes dans la table
        table.add_column("Option", justify="center", style="yellow")
        table.add_column("Action", style="green")

        # Options disponibles
        options = [
            ("1", "Ajouter un joueur"),
            ("2", "Afficher les joueurs du tournoi"),
            ("3", "Afficher les détails du tournoi"),
            ("4", "Démarrer le tournoi"),
            ("5", "Afficher les résultats des matchs"),
            ("6", "Modifier la description du tournoi"),
            ("0", "Retour au menu principal")
        ]

        for option in options:
            table.add_row(option[0], option[1])

        titre = Text(f"Menu Tournoi - {tournoi_nom}", style="bold cyan", justify="center")

        panel = Panel.fit(
            table,
            title = titre,
            border_style = "bright_blue",
            padding = (1, 2),
        )
        console.print(panel)

    def selectionner_option(self):
        choix = input("Veuillez sélectionner une option : ")
        return choix

    def menu_creer_joueurs(self, joueurs_controller):
        nom = input("Nom du joueur : ")
        prenom = input("Prènom du joueur : ")
        while True:
            date_naissance = joueurs_controller.verifier_dates("Date de naissance (YYYY/MM/DD) : ")
            if date_naissance > datetime.now().date():
                Rapport.afficher_message("Erreur : la date de naissance ne peut pas être postérieure à la date actuelle.")
                continue
            identifiant = input("Identifiant national : ")
            index = joueurs_controller.verifier_id(identifiant)
            if index == True:
                break
        date_naissance = date_naissance.strftime("%Y/%m/%d")
        joueurs_controller.ajouter_joueur(nom, prenom, date_naissance, identifiant)


    def menu_creer_tournoi(self, tournoi_controller, joueur_controller):
        nom = input("Nom du tournoi : ")
        lieu = input("Lieu : ")
        while True:
            date_debut = joueur_controller.verifier_dates("Date de début (YYYY/MM/DD) : ")
            if date_debut < datetime.now().date():
                print("Erreur : la date de début ne peut pas être antérieure à la date actuelle.")
                continue
            date_fin = joueur_controller.verifier_dates("Date de fin (YYYY/MM/DD) : ")
            if date_fin < date_debut:
                print("Erreur : la date de fin doit être postérieure à la date de début. Veuillez réessayer.")
            else:
                break
        date_debut = date_debut.strftime("%Y/%m/%d")
        date_fin = date_fin.strftime("%Y/%m/%d")
        description = input("Faire une desciption du tournoi : ")
        tournoi_controller.ajouter_tournoi(nom, lieu, date_debut, date_fin, description)