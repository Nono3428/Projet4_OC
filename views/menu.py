class Menu:
    def __init__(self):
        self.options = {
            "1": "Ajouter joueur",
            "2": "Liste des joueurs",
            "3": "Créer un nouveau tournoi",
            "4": "Liste des tournois",
            "5": "Sélectionner un tournoi",
            "0": "Quitter"
        }

    def afficher_menu(self):
        print("\n--- Menu Principal ---")
        for key, value in self.options.items():
            print(f"{key}: {value}")

    def afficher_menu_tournoi(self):
        print("\n=== Menu Tournoi ===")
        print("1. Ajouter un joueur")
        print("2. Afficher les joueurs du tournoi")
        print("3. Afficher les détails du tournoi")
        print("4. Démarer le tournoi")
        print("5. Afficher les résultats des matchs")
        print("6. Modifier la description du tournoi")
        print("0. Retour au menu principal")

    def selectionner_option(self):
        choix = input("Veuillez sélectionner une option : ")
        return choix
