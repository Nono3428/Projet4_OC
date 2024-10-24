from models.tournoi import Tournoi
from models.joueurs import Joueur
from views.rapport import Rapport
import random
import json

class TournoiController:
    def __init__(self, fichier_tournois):
        self.fichier_tournois = fichier_tournois
        self.tournois = self.charger_tournois(fichier_tournois)

    def ajouter_tournoi(self, nom, lieu, date_debut, date_fin, description, nombre_tours=4):
        tournoi = Tournoi(nom, lieu, date_debut, date_fin, description, nombre_tours)
        self.tournois.append(tournoi)
        self.sauvegarder_tournois()
        Rapport.afficher_message(f"Tournoi {nom} ajouté avec succès.")

    def ajouter_joueur_tournoi(self, tournoi, joueur):
        tournoi.ajouter_joueur(joueur)
        self.sauvegarder_tournois()

    def selectionner_tournoi(self, nom_tournoi):
        for tournoi in self.tournois:
            if tournoi.nom == nom_tournoi:
                return tournoi
        Rapport.afficher_message("Tournoi non trouvé.")
        return None
    
    def charger_tournois(self, fichier_tournois):
        with open(fichier_tournois, 'r') as fichier:
            tournois_data = json.load(fichier)
            tournois = []
            for tournoi in tournois_data:
                nom = tournoi.get('nom')
                lieu = tournoi.get('lieu')
                date_debut = tournoi.get('date_debut')
                date_fin = tournoi.get('date_fin')
                nombre_tours = tournoi.get('nombre_tours', 4)
                tour_actuel = tournoi.get('tour_actuel', 0)
                description = tournoi.get('description', "")
                joueurs_data = tournoi.get('joueurs', [])
                
                # Charge les joueurs
                joueurs = [Joueur(**joueur) for joueur in joueurs_data]
                
                # Création d'une instance de Tournoi
                tournois.append(Tournoi(nom, lieu, date_debut, date_fin, nombre_tours))
                tournois[-1].joueurs = joueurs  # Assigne les joueurs au tournoi
            return tournois

    def sauvegarder_tournois(self):
        with open(self.fichier_tournois, 'w') as f:
            json.dump([tournoi.to_dict() for tournoi in self.tournois], f, indent=4)
        Rapport.afficher_message("Les tournois ont été sauvegardés avec succès.")

    def afficher_tournois(self):
        Rapport.afficher_tournois(self.tournois)

    def ajouter_description(self):
        Tournoi.ajouter_description()

    def demarrer_tournoi(self, tournoi):
        tournoi.demarrer_tournoi()
        self.sauvegarder_tournois()

    # def demarrer_tournoi(self, data):
    #     """Démarre le tournoi en générant les tours."""
    #     for self.tour_actuel in range(self.nombre_tours):
    #         self.generer_tour()
    #         Rapport.afficher_message(f"Tour {self.tour_actuel} : ")

    #         self.gerer_resultats_tour(self.tours[-1])
    #         self.tour_actuel += 1

    #     # Afficher le classement final après tous les tours
    #     self.afficher_classement()