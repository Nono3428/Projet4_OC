from datetime import datetime
import re

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
        print("\n--- Menu Principal ---")
        for key, value in self.options.items():
            print(f"{key}: {value}")

    def afficher_menu_tournoi(self):
        print("\n=== Menu Tournoi ===")
        print("1. Ajouter un joueur")
        print("2. Afficher les joueurs du tournoi")
        print("3. Afficher les détails du tournoi")
        print("4. Démarer le tournoi")
        print("5. Afficher les résultats des matchs")
        print("6. Modifier la description du tournoi")
        print("0. Retour au menu principal")

    def selectionner_option(self):
        choix = input("Veuillez sélectionner une option : ")
        return choix


    def menu_creer_joueurs(self, joueurs_controller):
        nom = input("Nom du joueur : ")
        prenom = input("Prènom du joueur : ")
        date_naissance = joueurs_controller.verifier_dates("Date de naissance (YYYY/MM/DD) : ")
        while True:
            identifiant = input("Identifiant national : ")
            index, message = joueurs_controller.verifier_id(identifiant)
            if index:
                print("ok cbon")
                break
            else:
                print(f"Erreur : {message}")
        joueurs_controller.ajouter_joueur(nom, prenom, date_naissance, identifiant)


    def menu_creer_tournoi(self, tournoi_controller, joueur_controller):
        nom = input("Nom du tournoi : ")
        lieu = input("Lieu : ")
        while True:
            date_debut = joueur_controller.verifier_dates("Date de début (YYYY/MM/DD) : ")
            date_fin = joueur_controller.verifier_dates("Date de fin (YYYY/MM/DD) : ")
            if date_fin > date_debut:
                break
            else:
                print("Erreur : la date de fin doit être postérieure à la date de début. Veuillez réessayer.")
        description = input("Faire une desciption du tournoi : ")
        tournoi_controller.ajouter_tournoi(nom, lieu, date_debut, date_fin, description)