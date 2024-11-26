from .joueurs import Joueur
from .match import Match


class Tour:
    def __init__(self, numero):
        self.numero = numero
        self.matchs = []

    def ajouter_match(self, match):
        self.matchs.append(match)

    def to_dict(self):
        return {
            "numero": self.numero,
            "matchs": [match.to_dict() for match in self.matchs]
        }

    def from_dict(self, data):
        self.numero = data['numero']
        self.matchs = []
        for match_data in data.get('matchs', []):
            joueur1 = Joueur(match_data['joueur1'], "", "", match_data['joueur1'])
            joueur2 = Joueur(match_data['joueur2'], "", "", match_data['joueur2'])
            match = Match(joueur1, joueur2)
            match.score = match_data.get('score')
            self.ajouter_match(match)
