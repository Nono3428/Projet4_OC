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


    def menu_creer_joueurs(self, joueurs_controller):
        nom = input("Nom du joueur : ")
        prenom = input("Prènom du joueur : ")
        date_naissance = input("Date de naissance : ")
        identifiant = input("Identifiant national : ")
        joueurs_controller.ajouter_joueur(nom, prenom, date_naissance, identifiant)


    def menu_creer_tournoi(self, tournoi_controller):
        nom = input("Nom du tournoi : ")
        lieu = input("Lieu : ")
        date_debut = input("Date de début (YYYY-MM-DD) : ")
        date_fin = input("Date de fin (YYYY-MM-DD) : ")
        description = input("Faire une desciption du tournoi : ")
        tournoi_controller.ajouter_tournoi(nom, lieu, date_debut, date_fin, description)