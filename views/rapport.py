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
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre de tours : {tournoi.nombre_tours}")
        print(f"Tour courant : {tournoi.tour_actuel}")
        print(f"Description : {tournoi.description}")
        Rapport.afficher_listes_joueurs(tournoi.joueurs)

    @staticmethod
    def afficher_message(message):
        print(message)

    @staticmethod
    def afficher_classement(tournoi):
        # Crée une liste des scores à partir du dictionnaire des scores du tournoi
        classement = sorted(tournoi.joueurs, key=lambda j: tournoi.scores.get(j.identifiant, 0), reverse=True)
        
        Rapport.afficher_message("\n--- Classement du Tournoi ---")
        for index, joueur in enumerate(classement, start=1):
            # Récupérer le score à partir du dictionnaire des scores
            score = tournoi.scores.get(joueur.identifiant, 0)
            Rapport.afficher_message(f"{index}. {joueur.prenom} {joueur.nom} - Score: {score}")
    
    @staticmethod
    def afficher_tours_et_matchs(tournoi):
        if not tournoi.tours:
            print("Aucun tour n'a été enregistré pour ce tournoi.")
            return
        
        print(f"\n--- Tours du Tournoi {tournoi.nom} ---")
        for tour in tournoi.tours:
            print(f"\nTour {tour.numero}:")
            if not tour.matchs:
                print("Aucun match enregistré pour ce tour.")
            else:
                for match in tour.matchs:
                    joueur1 = match.joueur1
                    joueur2 = match.joueur2
                    print(f"Match: {joueur1.prenom} {joueur1.nom} vs {joueur2.prenom} {joueur2.nom}")
                    # Afficher les scores si disponibles
                    score_joueur1, score_joueur2 = match.score
                    if score_joueur1 is not None and score_joueur2 is not None:
                        print(f"Score: {score_joueur1} - {score_joueur2}")
                    else:
                        print("Score: Non enregistré.")
            