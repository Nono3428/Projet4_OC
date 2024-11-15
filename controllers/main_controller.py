from controllers.joueurs_controller import JoueursController
from controllers.tournoi_controller import TournoiController
from models.tournoi import Tournoi
from views.menu import Menu
from views.rapport import Rapport

class MainController:
    def __init__(self):
        self.joueurs_controller = JoueursController('data/joueurs.json')
        self.tournoi_controller = TournoiController('data/tournois.json')
        self.menu = Menu()

    def demarrer(self):
        while True:
            # Afficher le menu principal
            self.menu.afficher_menu()
            choix = self.menu.selectionner_option()

            if choix == "1":
                # Ajouter un joueur
                self.menu.menu_creer_joueurs(self.joueurs_controller)
            elif choix == "2":
                # Liste des joueurs
                self.joueurs_controller.listes_joueurs()
            elif choix == "3":
                # Créer un nouveau tournoi
                self.menu.menu_creer_tournoi(self.tournoi_controller, self.joueurs_controller)
            elif choix == "4":
                # Liste des tournois
                self.tournoi_controller.afficher_tournois()
            elif choix == "5":
                # Sélectionner un tournoi
                self.tournoi_controller.afficher_tournois()
                tournoi_nom = input("Nom du tournoi à sélectionner : ")
                tournoi = self.tournoi_controller.selectionner_tournoi(tournoi_nom)
                if tournoi:
                    while True:
                        self.menu.afficher_menu_tournoi(tournoi_nom)
                        choix_tournoi = self.menu.selectionner_option()

                        if choix_tournoi == "1":
                            # Ajouter un joueur au tournoi
                            Rapport.liste_joueurs(self.joueurs_controller.joueurs)
                            joueur_identifiant = input("Identifiant du joueur : ")
                            joueur = self.joueurs_controller.rechercher_joueur(joueur_identifiant)
                            if joueur:
                                self.tournoi_controller.ajouter_joueur_tournoi(tournoi, joueur, self.joueurs_controller)
                            else:
                                Rapport.afficher_message("Joueur non trouvé.")
                        elif choix_tournoi == "2":
                            # Afficher les joueurs du tournoi
                            Rapport.afficher_listes_joueurs(tournoi.joueurs)
                        elif choix_tournoi == "3":
                            # Afficher les détails du tournoi
                            Rapport.afficher_details_tournoi(tournoi)
                        elif choix_tournoi == "4":
                            # Démarer tournoi
                            if (tournoi.tour_actuel == tournoi.nombre_tours):
                                Rapport.afficher_message("Le tournoi est déjà terminer")
                            else:
                                self.tournoi_controller.demarrer_tournoi(tournoi, self.joueurs_controller)
                        elif choix_tournoi == "5":
                            # Afficher résultats
                            Rapport.afficher_tours_et_matchs(tournoi)
                            Rapport.afficher_classement(tournoi)
                        elif choix_tournoi == "6":
                            tournoi.ajouter_description(tournoi)
                        elif choix_tournoi == "0":
                            break  # Retour au menu principal
                        else:
                            Rapport.afficher_message("Choix invalide.")
                else:
                    Rapport.afficher_message("Tournoi non trouvé.")
            elif choix == "0":
                Rapport.afficher_message("Quitter le programme.")
                break
            else:
                Rapport.afficher_message("Option invalide.")
