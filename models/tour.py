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