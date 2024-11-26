from .tour import Tour
from ..views.rapport import Rapport
from .joueurs import Joueur
import json


class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, description, nombre_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.tour_actuel = 0
        self.tours = []
        self.joueurs = []
        self.description = description
        self.scores = {}

    def ajouter_joueur(self, joueur):
        self.joueurs.append(joueur)

    def ajouter_description(self):
        self.description = input("Faire une description du tournoi : ")

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "nombre_tours": self.nombre_tours,
            "tour_actuel": self.tour_actuel,
            "tours": [tour.to_dict() for tour in self.tours],
            "joueurs": [joueur.to_dict() for joueur in self.joueurs],
            "description": self.description,
            "scores": self.scores
        }

    @staticmethod
    def charger_tournois(fichier_tournois):
        with open(fichier_tournois, 'r') as fichier:
            tournois_data = json.load(fichier)
            tournois = []
            for tournoi in tournois_data:
                nom = tournoi.get('nom')
                lieu = tournoi.get('lieu')
                date_debut = tournoi.get('date_debut')
                date_fin = tournoi.get('date_fin')
                nombre_tours = tournoi.get('nombre_tours')
                tour_actuel = tournoi.get('tour_actuel')
                description = tournoi.get('description')
                joueurs_data = tournoi.get('joueurs', [])
                tours_data = tournoi.get('tours', [])
                scores = tournoi.get('scores', {})
                joueurs = [Joueur(**joueur) for joueur in joueurs_data]

                tournoi_instance = (Tournoi(nom, lieu, date_debut, date_fin, description, nombre_tours))
                tournoi_instance.tour_actuel = tour_actuel
                tournoi_instance.joueurs = joueurs
                tournoi_instance.scores = scores

                for tour_data in tours_data:
                    tour_instance = Tour(tour_data['numero'])
                    tour_instance.from_dict(tour_data)
                    tournoi_instance.tours.append(tour_instance)

                tournois.append(tournoi_instance)
            return tournois

    @staticmethod
    def sauvegarder_tournois(tournois, fichier_tournois):
        with open(fichier_tournois, 'w') as f:
            json.dump([tournoi.to_dict() for tournoi in tournois], f, indent=4)
        Rapport.afficher_message("Les tournois ont été sauvegardés avec succès.")
