class Match:
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score = None

    def definir_score(self, score_joueur1, score_joueur2):
        self.score = (score_joueur1, score_joueur2)

    def to_dict(self):
        return {
            "joueur1": self.joueur1.identifiant,
            "joueur2": self.joueur2.identifiant,
            "score": self.score
        }
