from models.tournoi import Tournoi
from models.tour import Tour
from models.match import Match
from models.joueurs import Joueur
from views.rapport import Rapport
import random

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

    def afficher_classement(tournoi):
        Rapport.afficher_classement(tournoi)

    def demarrer_tournoi(self, tournoi):
        """Démarre le tournoi en générant les tours."""
        if len(tournoi.joueurs) >= 6:
            self.generer_tour(tournoi)
            Rapport.afficher_message(f"Tour {tournoi.tour_actuel} : ")

            self.gerer_resultats_tour(tournoi.tours[-1], tournoi)
            tournoi.tour_actuel += 1

            # Afficher le classement final après tous les tours
            tournoi.afficher_classement()
            tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)
        else:
            Rapport.afficher_message("Il n'y a pas asser de participants pour le tournoi. Minimum de 6 participants pour lancer le tournoi.")

    def generer_tour(self, tournoi):
        """Génère un tour (premier ou suivant) en fonction des scores et des adversaires."""
        tour = Tour(tournoi.tour_actuel + 1)  # Créer un nouvel objet Tour

        if tournoi.tour_actuel == 0:
            print("Génération du premier tour : mélange aléatoire des joueurs.")
            random.shuffle(tournoi.joueurs)  # Mélanger les joueurs
        else:
            print("Génération du tour suivant : tri des joueurs par score.")
            tournoi.joueurs.sort(key=lambda j: tournoi.scores.get(j.identifiant, 0), reverse=True)  # Trier les joueurs par score

        paires_deja_jouees = set()  # Ensemble pour suivre les paires déjà jouées
        joueurs_non_appaires = tournoi.joueurs.copy()  # Copie de la liste des joueurs

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

        print(f"Type des éléments dans tournoi.tours : {[type(tour) for tour in tournoi.tours]}")
        tournoi.tours.append(tour)  # Ajouter le tour à la liste des tours
        print(f"Type des éléments dans tournoi.tours : {[type(tour) for tour in tournoi.tours]}")

        print(f"Tour {tournoi.tour_actuel + 1} généré avec succès.")

    def gerer_resultats_tour(self, tour, tournoi):
        print(f"Gérer les résultats pour le tour {tour.numero} :")
        for match in tour.matchs:  # Supposons que `tour.matchs` contient tous les matchs du tour
            joueur1 = match.joueur1
            joueur2 = match.joueur2
            while True:
                try:
                    # Saisie des résultats pour le match
                    score_joueur1 = int(input(f"Entrez le score de {joueur1.nom} {joueur1.prenom} : "))
                    score_joueur2 = int(input(f"Entrez le score de {joueur2.nom} {joueur2.prenom} : "))
                    
                    # Mise à jour des scores dans le tournoi
                    tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0) + score_joueur1
                    tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0) + score_joueur2
                    
                    match.definir_score(score_joueur1, score_joueur2)  # Assure-toi que Match a cette méthode
                    print(f"Match {joueur1.nom} {joueur1.prenom} ({score_joueur1}) - ({score_joueur2}) {joueur2.nom} {joueur2.prenom} enregistré.")
                    
                    break  # Sortir de la boucle une fois que le score a été correctement saisi
                
                except ValueError:
                    print("Veuillez entrer un nombre valide pour le score.")