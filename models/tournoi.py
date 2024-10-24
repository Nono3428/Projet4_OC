from datetime import datetime
from models.tour import Tour
from views.rapport import Rapport
from models.match import Match
import random

class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, description, nombre_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        self.date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
        self.nombre_tours = nombre_tours
        self.tour_actuel = 0
        self.tours = []
        self.joueurs = []
        self.description = description

    def demarrer_tournoi(self, data):
        """Démarre le tournoi en générant les tours."""
        for self.tour_actuel in range(self.nombre_tours):
            self.generer_tour()
            Rapport.afficher_message(f"Tour {self.tour_actuel} : ")

            self.gerer_resultats_tour(self.tours[-1])
            self.tour_actuel += 1

        # Afficher le classement final après tous les tours
        self.afficher_classement()

    def ajouter_joueur(self, joueur):
        self.joueurs.append(joueur)

    def ajouter_description(self):
        self.description = input("Faire une description du tournoi : ")

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_debut": self.date_debut.strftime("%Y-%m-%d"),
            "date_fin": self.date_fin.strftime("%Y-%m-%d"),
            "nombre_tours": self.nombre_tours,
            "tour_actuel" : self.tour_actuel,
            "tours": [tour.to_dict() for tour in self.tours],  # Assurez-vous que la classe Tour a une méthode to_dict aussi
            "joueurs": [joueur.to_dict() for joueur in self.joueurs],  # Assurez-vous que la classe Joueur a une méthode to_dict aussi
            "description": self.description
        }




    def demarrer_tournoi(self):
        """Démarre le tournoi en générant les tours."""
        for self.tour_actuel in range(self.nombre_tours):
            self.generer_tour()
            Rapport.afficher_message(f"Tour {self.tour_actuel} : ")

            self.gerer_resultats_tour(self.tours[-1])
            self.tour_actuel += 1

        # Afficher le classement final après tous les tours
        self.afficher_classement()



    def generer_tour(self):
        """Génère un tour (premier ou suivant) en fonction des scores et des adversaires."""
        tour = Tour(self.tour_actuel + 1)

        if self.tour_actuel == 0:
            print("premier tour")
            # Premier tour: Mélange aléatoire des joueurs
            random.shuffle(self.joueurs)
            for joueur in self.joueurs:
                joueur.adversaires = []  # Initialiser la liste des adversaires
        else:
            print('deuxieme tour')
            # Tours suivants: Trier les joueurs par score décroissant
            self.joueurs.sort(key=lambda j: j.score, reverse=True)

        joueurs_non_appaires = self.joueurs.copy()

        while joueurs_non_appaires:
            joueur1 = joueurs_non_appaires.pop(0)

            # Trouver un joueur qui n'a pas encore affronté joueur1
            for i, joueur2 in enumerate(joueurs_non_appaires):
                if joueur2.identifiant not in joueur1.adversaires:
                    # Ajouter l'adversaire aux deux joueurs
                    joueur1.adversaires.append(joueur2.identifiant)
                    joueur2.adversaires.append(joueur1.identifiant)

                    # Créer et ajouter un match
                    tour.ajouter_match(Match(joueur1, joueur2))

                    # Retirer joueur2 de la liste
                    joueurs_non_appaires.pop(i)
                    break

        self.tours.append(tour)
        self.tour_actuel += 1









    # def generer_premier_tour(self):
    #     """Génère le premier tour avec des paires aléatoires."""
    #     random.shuffle(self.joueurs)  # Mélanger les joueurs
    #     tour = Tour(self.tour_actuel + 1)  # Créer un nouveau tour

    #     for i in range(0, len(self.joueurs), 2):
    #         if i + 1 < len(self.joueurs):
    #             tour.ajouter_match(Match(self.joueurs[i], self.joueurs[i + 1]))

    #     self.tours.append(tour)

    # def generer_tour_suivant(self):
    #     """Génère le tour suivant en fonction des scores accumulés."""
    #     tour = Tour(self.tour_actuel + 1)
    #     self.joueurs.sort(key=lambda j: j.score, reverse=True)  # Trier les joueurs par score

    #     for i in range(0, len(self.joueurs), 2):
    #         if i + 1 < len(self.joueurs):
    #             tour.ajouter_match(Match(self.joueurs[i], self.joueurs[i + 1]))

    #     self.tours.append(tour)

    def gerer_resultats_tour(self, tour):
        for match in tour.matchs:
            Rapport.afficher_message(f"Match: {match.joueur1.prenom} vs {match.joueur2.prenom}")
            score_joueur1 = float(input(f"Entrez le score pour {match.joueur1.prenom} (0 pour perdre, 0.5 pour un match nul, 1 pour gagner) : "))
            score_joueur2 = 1 - score_joueur1  # Si joueur1 marque 1, joueur2 marque 0, etc.

            # Définir le score pour le match
            match.definir_score(score_joueur1, score_joueur2)

            # Mettre à jour les scores des joueurs
            match.joueur1.score += score_joueur1
            match.joueur2.score += score_joueur2

    def afficher_resultats(self):
        Rapport.afficher_message(f"\nRésultats après le tour {self.tour_actuel}:")
        for tour in self.tours:
            for match in tour.matchs:
                Rapport.afficher_message(f"Match: {match.joueur1.prenom} vs {match.joueur2.prenom}, Score: {match.score}")


    def afficher_classement(self):
        classement = sorted(self.joueurs, key=lambda j: j.score, reverse=True)
        
        Rapport.afficher_message("\n--- Classement Final du Tournoi ---")
        for index, joueur in enumerate(classement, start=1):
            Rapport.afficher_message(f"{index}. {joueur.prenom} {joueur.nom} - Score: {joueur.score}")
            # joueur.ajouter_tournoi(self.nom, joueur.score, self.date_debut, self.date_fin)
