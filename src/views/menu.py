from datetime import datetime
from .rapport import Rapport
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class Menu:
    def __init__(self):
        self.options = {
            "1": "Créer un nouveau joueur",
            "2": "Liste des joueurs",
            "3": "Créer un nouveau tournoi",
            "4": "Liste des tournois",
            "5": "Sélectionner un tournoi",
            "0": "Quitter"
        }

    def afficher_menu(self):
        console = Console()

        titre = Text("Menu Principal", style="bold cyan", justify="center")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", justify="center", style="yellow")
        table.add_column("Action", style="green")
        for key, action in self.options.items():
            table.add_row(key, action)
        panel = Panel.fit(
            table,
            title=titre,
            border_style="bright_blue",
            padding=(1, 2)
        )
        console.print(panel)

    def afficher_menu_tournoi(self, tournoi_nom):
        console = Console()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", justify="center", style="yellow")
        table.add_column("Action", style="green")

        options = [
            ("1", "Ajouter un joueur"),
            ("2", "Afficher les joueurs du tournoi"),
            ("3", "Afficher les détails du tournoi"),
            ("4", "Jouer un tour"),
            ("5", "Afficher les résultats des matchs"),
            ("6", "Modifier la description du tournoi"),
            ("0", "Retour au menu principal")
        ]

        for option in options:
            table.add_row(option[0], option[1])
        titre = Text(f"Menu Tournoi - {tournoi_nom}", style="bold cyan", justify="center")
        panel = Panel.fit(
            table,
            title=titre,
            border_style="bright_blue",
            padding=(1, 2),
        )
        console.print(panel)

    def selectionner_option(self):
        choix = input("Veuillez sélectionner une option : ")
        return choix

    def menu_creer_joueurs(self, joueurs_controller):
        nom = input("Nom du joueur : ")
        prenom = input("Prènom du joueur : ")
        while True:
            date_naissance = self.verifier_dates("Date de naissance (YYYY/MM/DD) : ")
            if date_naissance > datetime.now().date():
                Rapport.afficher_message("Erreur : la date de naissance ne peut pas être postérieure"
                                         "à la date actuelle.")
                continue
            while True:
                identifiant = input("Identifiant national : ")
                index = joueurs_controller.verifier_id(identifiant)
                if index:
                    break
            break
        date_naissance = date_naissance.strftime("%Y/%m/%d")
        joueurs_controller.ajouter_joueur(nom, prenom, date_naissance, identifiant)

    def menu_creer_tournoi(self, tournoi_controller, joueur_controller):
        nom = input("Nom du tournoi : ")
        lieu = input("Lieu : ")
        while True:
            date_debut = self.verifier_dates("Date de début (YYYY/MM/DD) : ")
            if date_debut < datetime.now().date():
                Rapport.afficher_message("Erreur : la date de début ne peut pas être antérieure à la date actuelle.")
                continue
            date_fin = self.verifier_dates("Date de fin (YYYY/MM/DD) : ")
            if date_fin < date_debut:
                Rapport.afficher_message("Erreur : la date de fin doit être postérieure à la date de début."
                                         " Veuillez réessayer.")
            else:
                break
        date_debut = date_debut.strftime("%Y/%m/%d")
        date_fin = date_fin.strftime("%Y/%m/%d")
        description = input("Faire une desciption du tournoi : ")
        tournoi_controller.ajouter_tournoi(nom, lieu, date_debut, date_fin, description)

    def verifier_dates(self, string):
        while True:
            date = input(string)
            try:
                date = datetime.strptime(date, "%Y/%m/%d")
                return date.date()
            except ValueError:
                Rapport.afficher_message("Erreur : Format de date non valide. Format requis : (YYYY/MM/DD)")
