import json
import os

class Joueur:
    def __init__(self, nom, prenom, date_naissance, identifiant, tournois_participes=[]):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.identifiant = identifiant
        self.tournois_participes = tournois_participes 
        self.score = 0

    def ajouter_tournoi(self, tournoi_nom, points, tournoi_date_debut, tournoi_date_fin):
        self.tournois_participes.append({
            'tournoi': tournoi_nom,
            'points': points,
            'date_debut': tournoi_date_debut,
            'date_fin': tournoi_date_fin
        })

    def to_dict(self):
        return {
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance,
            'identifiant': self.identifiant,
            'tournois_participes': self.tournois_participes,
        }
