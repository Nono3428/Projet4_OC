from models.tournoi import Tournoi
from models.joueurs import Joueur
from views.rapport import Rapport
import random
import json

class TournoiController:
    def __init__(self, fichier_tournois):
        self.fichier_tournois = fichier_tournois
        self.tournois = Tournoi.charger_tournois(fichier_tournois)

    def ajouter_tournoi(self, nom, lieu, date_debut, date_fin, description, nombre_tours=4):
        tournoi = Tournoi(nom, lieu, date_debut, date_fin, description, nombre_tours)
        self.tournois.append(tournoi)
        Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)
        Rapport.afficher_message(f"Tournoi {nom} ajouté avec succès.")

    def ajouter_joueur_tournoi(self, tournoi, joueur):
        tournoi.ajouter_joueur(joueur)
        Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)

    def selectionner_tournoi(self, nom_tournoi):
        for tournoi in self.tournois:
            if tournoi.nom == nom_tournoi:
                return tournoi
        Rapport.afficher_message("Tournoi non trouvé.")
        return None

    def afficher_tournois(self):
        Rapport.afficher_tournois(self.tournois)

    def ajouter_description(self):
        Tournoi.ajouter_description()

    def demarrer_tournoi(self, tournoi):
        tournoi.demarrer_tournoi()
        Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)

    # def demarrer_tournoi(self, data):
    #     """Démarre le tournoi en générant les tours."""
    #     for self.tour_actuel in range(self.nombre_tours):
    #         self.generer_tour()
    #         Rapport.afficher_message(f"Tour {self.tour_actuel} : ")

    #         self.gerer_resultats_tour(self.tours[-1])
    #         self.tour_actuel += 1

    #     # Afficher le classement final après tous les tours
    #     self.afficher_classement()