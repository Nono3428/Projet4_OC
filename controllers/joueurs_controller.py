import json
import re
from datetime import datetime
from models.joueurs import Joueur
from views.rapport import Rapport

class JoueursController:
    def __init__(self, fichier_joueurs):
        self.fichier_joueurs = fichier_joueurs
        self.joueurs = self.charger_joueurs(fichier_joueurs)
        self.liste_identifiants = self.charger_id_joueurs()

    def ajouter_joueur(self, nom, prenom, date_naissance, identifiant):
        nouveau_joueur = Joueur(nom, prenom, date_naissance, identifiant)
        self.joueurs.append(nouveau_joueur)
        self.liste_identifiants.add(identifiant)
        self.sauvegarder_joueurs()
        Rapport.afficher_message(f"Joueur {nom} {prenom} ajouté avec succès.")

    def charger_joueurs(self, fichier):
        try:
            with open(fichier, 'r') as f:
                data = f.read()
                if data:
                    joueurs_data = json.loads(data)
                    return [Joueur(**joueur) for joueur in joueurs_data]
                else:
                    Rapport.afficher_message("Le fichier des joueurs est vide. Aucun joueur chargé.")
                    return []
        except FileNotFoundError:
            Rapport.afficher_message("Le fichier des joueurs n'a pas été trouvé.")
            return []
        except json.JSONDecodeError:
            Rapport.afficher_message("Erreur lors de la lecture du fichier JSON des joueurs.")
            return []

    def sauvegarder_joueurs(self):
        with open(self.fichier_joueurs, 'w') as f:
            json.dump([joueur.to_dict() for joueur in self.joueurs], f, indent=4)
        Rapport.afficher_message("Les joueurs ont été sauvegardés avec succès.")
    
    def rechercher_joueur(self, identifiant):
        """Recherche un joueur par son identifiant national d'échecs."""
        for joueur in self.joueurs:
            if joueur.identifiant == identifiant:
                return joueur
        return None

    # def afficher_joueurs(self):
    #     Rapport.afficher_joueurs(self.joueurs)    

    # def afficher_details_joueurs(self):
    #     Rapport.afficher_details_joueur(self.joueurs)

    def listes_joueurs(self):
        Rapport.afficher_listes_joueurs(self.joueurs)

    def ajouter_tournoi_participees(self, tournoi, joueur):
        joueur.ajouter_tournoi(tournoi.nom, 0, tournoi.date_debut, tournoi.date_fin)
        self.sauvegarder_joueurs()

    def charger_id_joueurs(self):
        liste = set()
        for joueur in self.joueurs:
            liste.add(joueur.identifiant)
        return liste
    
    def verifier_dates(self, string):
        while True:
            date = input(string)
            try:
                date = datetime.strptime(date, "%Y/%m/%d")
                return date.date()
            except ValueError:
                print("Erreur : Format de date non valide. Format requis : (YYYY/MM/DD)")
            
    def verifier_id(self, identifiant):
        if not re.match("^[A-Za-z]{2}[0-9]{5}$", identifiant):
            Rapport.afficher_message("L'identifiant doit comporter deux lettres suivies de cinq chiffres, comme 'AB12345'.")
            return False

        if identifiant in self.liste_identifiants:
                Rapport.afficher_message("Cet identifiant existe déjà. Veuillez en choisir un autre.")
                return False

        return True