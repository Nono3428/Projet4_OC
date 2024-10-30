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
        Rapport.afficher_message(f"Tournoi {nom} ajouté avec succès.")
        Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)

    def ajouter_joueur_tournoi(self, tournoi, joueur):
        for j in tournoi.joueurs:
            if j.identifiant == joueur.identifiant:
                print(f"Le joueur {joueur.prenom} {joueur.nom} est déjà inscrit dans le tournoi.")
                break
        else:
            # Ajoute le joueur si pas encore dans la liste
            tournoi.ajouter_joueur(joueur)
            joueur.ajouter_tournoi(tournoi.nom, 0, tournoi.date_debut, tournoi.date_fin)
            Tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)
            print(f"Joueur {joueur.prenom} {joueur.nom} ajouté au tournoi avec succès.")


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
            self.gerer_resultats_tour(tournoi.tours[-1], tournoi)
            tournoi.tour_actuel += 1
            Rapport.afficher_classement(tournoi)
            tournoi.sauvegarder_tournois(self.tournois, self.fichier_tournois)
        else:
            Rapport.afficher_message("Il n'y a pas asser de participants pour le tournoi. Minimum de 6 participants pour lancer le tournoi.")

    def generer_tour(self, tournoi):
        """Génère un tour (premier ou suivant) en fonction des scores et des adversaires."""
        tour = Tour(tournoi.tour_actuel + 1)

        if tournoi.tour_actuel == 0:
            print("Génération du premier tour : mélange aléatoire des joueurs.")
            random.shuffle(tournoi.joueurs)
        else:
            print("Génération du tour suivant : tri des joueurs par score.")
            tournoi.joueurs.sort(key=lambda j: tournoi.scores.get(j.identifiant, 0), reverse=True)

        paires_deja_jouees = set()
        joueurs_non_appaires = tournoi.joueurs.copy()

        while len(joueurs_non_appaires) >= 2:
            joueur1 = joueurs_non_appaires.pop(0)

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
                    break

        tournoi.tours.append(tour)

        print(f"Paires pour le tour {tournoi.tour_actuel + 1} généré avec succès.")

    def gerer_resultats_tour(self, tour, tournoi):
        print(f"Gérer les résultats pour le tour {tour.numero} :")
        for match in tour.matchs:
            joueur1 = match.joueur1
            joueur2 = match.joueur2
            while True:
                try:
                    resultat = int(input(f"Qui est le vainqueur pour le match {joueur1.nom} {joueur1.prenom} vs {joueur2.nom} {joueur2.prenom} ? (1 = {joueur1.nom}, 2 = {joueur2.nom}, 0 = Match nul) : "))
                    
                    if resultat not in [0, 1, 2]:
                        print("Veuillez entrer un choix valide (1, 2, ou 0).")
                        continue

                    if resultat == 1:
                        tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0) + 1
                        tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0)
                        match.definir_score(1, 0)  # 1 point pour joueur1, 0 pour joueur2
                        print(f"{joueur1.nom} {joueur1.prenom} gagne contre {joueur2.nom} {joueur2.prenom}")
                    elif resultat == 2:
                        tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0)
                        tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0) + 1
                        match.definir_score(0, 1)  # 0 point pour joueur1, 1 pour joueur2
                        print(f"{joueur2.nom} {joueur2.prenom} gagne contre {joueur1.nom} {joueur1.prenom}")
                    else:  # Cas de match nul
                        tournoi.scores[joueur1.identifiant] = tournoi.scores.get(joueur1.identifiant, 0) + 0.5
                        tournoi.scores[joueur2.identifiant] = tournoi.scores.get(joueur2.identifiant, 0) + 0.5
                        match.definir_score(0.5, 0.5)  # 0.5 point pour chaque joueur
                        print(f"Match nul entre {joueur1.nom} {joueur1.prenom} et {joueur2.nom} {joueur2.prenom}")

                    joueur1.mettre_a_jour_points_tournoi(tournoi.nom, tournoi.scores[joueur1.identifiant])
                    joueur2.mettre_a_jour_points_tournoi(tournoi.nom, tournoi.scores[joueur2.identifiant])

                    break

                except ValueError:
                    print("Veuillez entrer un nombre valide (1 pour victoire joueur1, 2 pour victoire joueur2, 0 pour match nul).")
