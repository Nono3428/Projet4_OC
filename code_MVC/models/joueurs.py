import json
from views.rapport import Rapport


class Joueur:
    def __init__(self, nom, prenom, date_naissance, identifiant, tournois_participes=[]):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.identifiant = identifiant
        self.tournois_participes = tournois_participes

    def ajouter_tournoi(self, tournoi_nom, points, tournoi_date_debut, tournoi_date_fin):
        self.tournois_participes.append({
            'tournoi': tournoi_nom,
            'points': points,
            'date_debut': tournoi_date_debut,
            'date_fin': tournoi_date_fin
        })

    def mettre_a_jour_points_tournoi(self, tournoi_nom, nouveaux_points):
        for tournoi in self.tournois_participes:
            if tournoi['tournoi'] == tournoi_nom:
                tournoi['points'] = nouveaux_points
                return
            else:
                print(f"Le joueur n'est pas inscrit au tournoi '{tournoi_nom}'.")

    def to_dict(self):
        return {
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance,
            'identifiant': self.identifiant,
            'tournois_participes': self.tournois_participes,
        }

    @staticmethod
    def charger_joueurs(fichier):
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

    @staticmethod
    def sauvegarder_joueurs(joueurs, fichier_joueurs):
        with open(fichier_joueurs, 'w') as f:
            json.dump([joueur.to_dict() for joueur in joueurs], f, indent=4)
        Rapport.afficher_message("Les joueurs ont été sauvegardés avec succès.")
