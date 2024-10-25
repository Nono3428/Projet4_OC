class Rapport:  

    @staticmethod
    def afficher_listes_joueurs(joueurs):
        if not joueurs:
            print("Aucun joueur enregistré.")
            return
        choix = input("Voulez vous une liste détaillées des joueurs (oui/non): ")
        while choix != 'oui' or choix != 'non':
            if choix == "oui":
                for joueur in joueurs:
                    print(f"\n=== Détails de {joueur.nom} {joueur.prenom} ===")
                    print(f"Date de naissance: {joueur.date_naissance}")
                    print(f"Identifiant National : {joueur.identifiant}")
                    print("Tournois participés:")
                    for tournoi in joueur.tournois_participes:
                        print(f"- {tournoi['tournoi']} (Points: {tournoi['points']}, Dates: {tournoi['date_debut']} à {tournoi['date_fin']})")
                return    
            elif choix == "non":
                joueurs_tries = sorted(joueurs, key=lambda joueur: joueur.nom)
                print("\n=== Liste des Joueurs ===")
                for joueur in joueurs_tries:
                    print(f"{joueur.nom} {joueur.prenom} - ID: {joueur.identifiant}")
                return
            else:       
                choix = input("Veuillez saisir 'oui' ou 'non' !:")

    @staticmethod
    def afficher_joueurs(joueurs):
        if not joueurs:
            print("Aucun joueur enregistré.")
            return
        joueurs_tries = sorted(joueurs, key=lambda joueur: joueur.nom)
        print("\n=== Liste des Joueurs ===")
        for joueur in joueurs_tries:
            print(f"{joueur.nom} {joueur.prenom} - ID: {joueur.identifiant}")

    @staticmethod
    def afficher_details_joueur(joueurs):
        if joueurs:
            print('je suis la !!!')
            for joueur in joueurs:
                print(f"\n=== Détails de {joueur.nom} {joueur.prenom} ===")
                print(f"Date de naissance: {joueur.date_naissance}")
                print(f"Identifiant National : {joueur.identifiant}")
                print("Tournois participés:")
                for tournoi in joueur.tournois_participes:
                    print(f"- {tournoi['tournoi']} (Points: {tournoi['points']}, Dates: {tournoi['date_debut']} à {tournoi['date_fin']})")
        else:
            print("Joueur non trouvé.")

    @staticmethod
    def afficher_tournois(tournois):
        if not tournois:
            print("Aucun tournoi enregistré.")
            return
        print("\n=== Liste des Tournois ===")
        for tournoi in tournois:
            print(f"{tournoi.nom} - Lieu: {tournoi.lieu}, Dates: {tournoi.date_debut} à {tournoi.date_fin}")
    
    @staticmethod
    def afficher_details_tournoi(tournoi):
        print("\n=== Détails du Tournoi ===")
        print(f"Nom : {tournoi.nom}")
        print(f"Lieu : {tournoi.lieu}")
        print(f"Date de début : {tournoi.date_debut.strftime('%Y-%m-%d')}")
        print(f"Date de fin : {tournoi.date_fin.strftime('%Y-%m-%d')}")
        print(f"Nombre de tours : {tournoi.nombre_tours}")
        print(f"Tour courant : {tournoi.tour_actuel}")
        print(f"Description : {tournoi.description}")
        # print(f"Liste des joueurs : {tournoi.joueurs}")
        Rapport.afficher_details_joueur(tournoi.joueurs)

    @staticmethod
    def afficher_message(message):
        print(message)