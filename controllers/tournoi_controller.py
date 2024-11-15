from models.tournoi import Tournoi
from models.tour import Tour
from models.match import Match
from models.joueurs import Joueur
from views.rapport import Rapport
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

class TournoiController:
    def __init__(self, fichier_tournois):
        self.fichier_tournois = fichier_tournois
        self.tournois = Tournoi.charger_tournois(fichier_tournois)

    def ajouter_tournoi(self, nom, lieu, date_debut, date_fin, description, nombre_tours=4):
        tournoi = Tournoi(nom, lieu, date_debut, date_fin, description, nombre_tours)
        self.tournois.append(tournoi)
        Rapport.afficher_message(f"Tournoi {nom} ajouté avec succès.")
        Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)

    def ajouter_joueur_tournoi(self, tournoi, joueurs, joueur_controller):
        for joueur in tournoi.joueurs:
            if joueur.identifiant == joueurs.identifiant:
                Rapport.afficher_message(f"Le joueur {joueurs.prenom} {joueurs.nom} est déjà inscrit dans le tournoi.")
                break
        else:
            # Ajoute le joueur si pas encore dans la liste
            tournoi.ajouter_joueur(joueurs)
            joueurs.ajouter_tournoi(tournoi.nom, 0, tournoi.date_debut, tournoi.date_fin)
            Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)
            Joueur.sauvegarder_joueurs(joueur_controller.joueurs, joueur_controller.fichier_joueurs)
            Rapport.afficher_message(f"Joueur {joueurs.prenom} {joueurs.nom} ajouté au tournoi avec succès.")

    def selectionner_tournoi(self, nom_tournoi):
        for tournoi in self.tournois:
            if tournoi.nom == nom_tournoi:
                return tournoi
        return None

    def afficher_tournois(self):
        Rapport.afficher_tournois(self.tournois)

    def ajouter_description(self, tournoi):
        tournoi.ajouter_description()

    def demarrer_tournoi(self, tournoi, joueur_controller):
        """Démarre le tournoi en générant les tours."""
        if len(tournoi.joueurs) >= 6:
            self.generer_tour(tournoi)
            self.gerer_resultats_tour(tournoi.tours[-1], tournoi, joueur_controller)
            tournoi.tour_actuel += 1
            Rapport.afficher_classement(tournoi)
            tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)
            Joueur.sauvegarder_joueurs(joueur_controller.joueurs, joueur_controller.fichier_joueurs)
        else:
            Rapport.afficher_message("Il n'y a pas asser de participants pour le tournoi. Minimum de 6 participants pour lancer le tournoi.")

    def generer_tour(self, tournoi):
        """Génère un tour (premier ou suivant) en fonction des scores et des adversaires."""
        tour = Tour(tournoi.tour_actuel + 1)

        if tournoi.tour_actuel == 0:
            Rapport.afficher_message("Génération du premier tour : mélange aléatoire des joueurs.")
            random.shuffle(tournoi.joueurs)
        else:
            Rapport.afficher_message("Génération du tour suivant : tri des joueurs par score.")
            tournoi.joueurs.sort(key=lambda j: tournoi.scores.get(j.identifiant, 0), reverse=True)

        paires_deja_jouees = set()
        joueurs_non_appaires = tournoi.joueurs.copy()

        while len(joueurs_non_appaires) >= 2:
            joueur1 = joueurs_non_appaires.pop(0)

            # Trouver un joueur qui n'a pas encore affronté joueur1
            for i, joueur2 in enumerate(joueurs_non_appaires):
                if (joueur1.identifiant, joueur2.identifiant) not in paires_deja_jouees and \
                   (joueur2.identifiant, joueur1.identifiant) not in paires_deja_jouees:

                    # Ajouter la paire à l'ensemble des paires déjà jouées
                    paires_deja_jouees.add((joueur1.identifiant, joueur2.identifiant))

                    # Créer et ajouter un match
                    tour.ajouter_match(Match(joueur1, joueur2))
                    
                    # Retirer joueur2 de la liste
                    joueurs_non_appaires.pop(i)
                    break

        tournoi.tours.append(tour)

        Rapport.afficher_message(f"Paires pour le tour {tournoi.tour_actuel + 1} généré avec succès.")

    def gerer_resultats_tour(self, tour, tournoi):
        console = Console()
        console.print(Panel(f"[bold cyan]Gérer les résultats pour le Tour {tour.numero}[/bold cyan]", expand=False))

        for match in tour.matchs:
            joueur1 = match.joueur1
            joueur2 = match.joueur2

            # Table d'affichage du match
            table = Table(title="Détails du Match", expand=True, show_header=True)
            table.add_column("Joueur 1", justify="center", style="bold")
            table.add_column("Contre", justify="center", style="bold")
            table.add_column("Joueur 2", justify="center", style="bold")

            table.add_row(f"{joueur1.prenom} {joueur1.nom}", "VS", f"{joueur2.prenom} {joueur2.nom}")
            console.print(table)
            # Gestion du résultat avec une boucle de validation
            while True:
                try:
                    resultat = IntPrompt.ask(f"[yellow]Qui est le vainqueur pour ce match ?[/yellow]\n(1 = {joueur1.nom}, 2 = {joueur2.nom}, 0 = Match nul)")
                    
                    # Vérification du choix de l’utilisateur
                    if resultat not in [0, 1, 2]:
                        console.print("[red]Veuillez entrer un choix valide (1, 2 ou 0).[/red]")
                        continue

                    # Mise à jour des scores en fonction du résultat
                    if resultat == 1:
                        tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0) + 1
                        tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0)
                        match.definir_score(1, 0)
                        console.print(f"[green]{joueur1.nom} {joueur1.prenom} gagne contre {joueur2.nom} {joueur2.prenom}[/green]")

                    elif resultat == 2:
                        tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0)
                        tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0) + 1
                        match.definir_score(0, 1)
                        console.print(f"[green]{joueur2.nom} {joueur2.prenom} gagne contre {joueur1.nom} {joueur1.prenom}[/green]")

                    else:  # Match nul
                        tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0) + 0.5
                        tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0) + 0.5
                        match.definir_score(0.5, 0.5)
                        console.print(f"[blue]Match nul entre {joueur1.nom} {joueur1.prenom} et {joueur2.nom} {joueur2.prenom}[/blue]")

                    # Mettre à jour les points des joueurs
                    joueur1.mettre_a_jour_points_tournoi(tournoi.nom, tournoi.scores[joueur1.identifiant])
                    joueur2.mettre_a_jour_points_tournoi(tournoi.nom, tournoi.scores[joueur2.identifiant])
                    break

                except ValueError:
                    console.print("[red]Entrée invalide. Veuillez entrer 1 pour le joueur 1, 2 pour le joueur 2, ou 0 pour match nul.[/red]")