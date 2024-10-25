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
                # nom = input("Nom du joueur : ")
                # prenom = input("Prènom du joueur : ")
                # date_naissance = input("Date de naissance : ")
                # identifiant = input("Identifiant national : ")
                # self.joueurs_controller.ajouter_joueur(nom, prenom, date_naissance, identifiant)
                self.menu.menu_creer_joueurs(self.joueurs_controller)
            elif choix == "2":
                # Liste des joueurs
                    # if input("Voulez vous une liste détaillées des joueurs (oui/non): ") == "oui":
                    #     self.joueurs_controller.afficher_details_joueurs()
                    # else:
                    #     self.joueurs_controller.afficher_joueurs()
                    self.joueurs_controller.listes_joueurs()
            elif choix == "3":
                # Créer un nouveau tournoi
                # nom = input("Nom du tournoi : ")
                # lieu = input("Lieu : ")
                # date_debut = input("Date de début (YYYY-MM-DD) : ")
                # date_fin = input("Date de fin (YYYY-MM-DD) : ")
                # description = input("Faire une desciption du tournoi : ")
                # self.tournoi_controller.ajouter_tournoi(nom, lieu, date_debut, date_fin, description)
                self.menu.menu_creer_tournoi(self.tournoi_controller)
            elif choix == "4":
                # Liste des tournois
                self.tournoi_controller.afficher_tournois()
            elif choix == "5":
                # Sélectionner un tournoi
                tournoi_nom = input("Nom du tournoi à sélectionner : ")
                tournoi = self.tournoi_controller.selectionner_tournoi(tournoi_nom)
                print("tournoi === ", tournoi)
                if tournoi:
                    while True:
                        self.menu.afficher_menu_tournoi()
                        choix_tournoi = self.menu.selectionner_option()

                        if choix_tournoi == "1":
                            # Ajouter un joueur au tournoi
                            joueur_identifiant = input("Identifiant du joueur : ")
                            joueur = self.joueurs_controller.rechercher_joueur(joueur_identifiant)
                            if joueur:
                                self.tournoi_controller.ajouter_joueur_tournoi(tournoi, joueur)
                                Rapport.afficher_message(f"{joueur.nom} {joueur.prenom} ajouté au tournoi.")
                            else:
                                Rapport.afficher_message("Joueur non trouvé.")
                        elif choix_tournoi == "2":
                            # Afficher les joueurs du tournoi
                            Rapport.afficher_joueurs(tournoi.joueurs)
                        elif choix_tournoi == "3":
                            # Afficher les détails du tournoi
                            Rapport.afficher_details_tournoi(tournoi)
                        elif choix_tournoi == "4":
                            # Démarer tournoi
                            self.tournoi_controller.demarrer_tournoi(tournoi)
                        elif choix_tournoi == "5":
                            # Afficher résultats
                            self.tournoi_controller.afficher_tournois()
                        elif choix_tournoi == "6":
                            tournoi.ajouter_description()
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

