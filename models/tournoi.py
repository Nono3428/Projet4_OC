from datetime import datetime
from models.tour import Tour
from views.rapport import Rapport
from models.match import Match
from models.joueurs import Joueur
import random
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
            "tour_actuel" : self.tour_actuel,
            "tours": [tour.to_dict() for tour in self.tours],
            "joueurs": [joueur.to_dict_tournoi() for joueur in self.joueurs],
            "description": self.description
        }

    def demarrer_tournoi(self):
        """Démarre le tournoi en générant les tours."""
        paires_deja_jouees = set()
        for self.tour_actuel in range(self.nombre_tours):
            self.generer_tour()
            Rapport.afficher_message(f"Tour {self.tour_actuel} : ")

            self.gerer_resultats_tour(self.tours[-1])
            self.tour_actuel += 1

        # Afficher le classement final après tous les tours
        self.afficher_classement()

    def generer_tour(self):
        """Génère un tour (premier ou suivant) en fonction des scores et des adversaires."""
        tour = Tour(self.tour_actuel + 1)  # Créer un nouvel objet Tour

        if self.tour_actuel == 0:
            print("Génération du premier tour : mélange aléatoire des joueurs.")
            random.shuffle(self.joueurs)  # Mélanger les joueurs
        else:
            print("Génération du tour suivant : tri des joueurs par score.")
            self.joueurs.sort(key=lambda j: j.score, reverse=True)  # Trier les joueurs par score

        paires_deja_jouees = set()  # Ensemble pour suivre les paires déjà jouées
        joueurs_non_appaires = self.joueurs.copy()  # Copie de la liste des joueurs

        while len(joueurs_non_appaires) >= 2:  # S'assurer qu'il y a au moins 2 joueurs à apparier
            joueur1 = joueurs_non_appaires.pop(0)  # Prendre le premier joueur

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
                    break  # Sortir de la boucle une fois que l'adversaire est trouvé

        self.tours.append(tour)  # Ajouter le tour à la liste des tours
        print(f"Tour {self.tour_actuel + 1} généré avec succès.")

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
        # for match in tour.matchs:
        #     Rapport.afficher_message(f"Match: {match.joueur1.prenom} vs {match.joueur2.prenom}")
        #     score_joueur1 = float(input(f"Entrez le score pour {match.joueur1.prenom} (0 pour perdre, 0.5 pour un match nul, 1 pour gagner) : "))
        #     score_joueur2 = 1 - score_joueur1  # Si joueur1 marque 1, joueur2 marque 0, etc.

        #     # Définir le score pour le match
        #     match.definir_score(score_joueur1, score_joueur2)

        #     # Mettre à jour les scores des joueurs
        #     match.joueur1.score += score_joueur1
        #     match.joueur2.score += score_joueur2
        print(f"Gérer les résultats pour le tour {tour.numero} :")
        for match in tour.matchs:  # Supposons que `tour.matchs` contient tous les matchs du tour
            joueur1 = match.joueur1
            joueur2 = match.joueur2
            print(f"=== Match entre {joueur1.nom} {joueur1.prenom} et {joueur2.nom} {joueur2.prenom}. === ")
            while True:
                try:
                    # Saisie des résultats pour le match
                    score_joueur1 = int(input(f"Entrez le score de {joueur1.nom} {joueur1.prenom} : "))
                    score_joueur2 = int(input(f"Entrez le score de {joueur2.nom} {joueur2.prenom} : "))
                    
                    # Mise à jour des scores
                    joueur1.score += score_joueur1
                    joueur2.score += score_joueur2

                    # Afficher les résultats du match
                    print(f"Match {joueur1.nom} {joueur1.prenom} ({score_joueur1}) - ({score_joueur2}) {joueur2.nom} {joueur2.prenom} enregistré.")
                    
                    break  # Sortir de la boucle une fois que le score a été correctement saisi
                
                except ValueError:
                    print("Veuillez entrer un nombre valide pour le score.")

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
                description = tournoi.get('description', "")
                joueurs_data = tournoi.get('joueurs', [])
                
                # Charge les joueurs
                joueurs = [Joueur(**joueur) for joueur in joueurs_data]
                
                # Création d'une instance de Tournoi
                tournois.append(Tournoi(nom, lieu, date_debut, date_fin, nombre_tours))
                tournois[-1].joueurs = joueurs  # Assigne les joueurs au tournoi
            return tournois

    @staticmethod
    def sauvegarder_tournois(tournois, fichier_tournois):
        with open(fichier_tournois, 'w') as f:
            json.dump([tournoi.to_dict() for tournoi in tournois], f, indent=4)
        Rapport.afficher_message("Les tournois ont été sauvegardés avec succès.")