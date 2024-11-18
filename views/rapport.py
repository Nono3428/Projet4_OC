from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
class Rapport:  

    @staticmethod
    def afficher_listes_joueurs(joueurs):
        console = Console()
        if not joueurs:
            console.print("[bold red]Aucun joueurs enregistré.[/bold red]")
            return
        choix = input("Voulez vous une liste détaillées des joueurs (oui/non): ")
        joueurs_tries = sorted(joueurs, key=lambda joueur: joueur.nom)
        while choix != 'oui' or choix != 'non':
            if choix == "oui":
                Rapport.afficher_details_joueur(joueurs_tries)
                return
            elif choix == "non":
                Rapport.liste_joueurs(joueurs_tries)
                return
            else:       
                choix = input("Veuillez saisir 'oui' ou 'non' !:")

    @staticmethod
    def liste_joueurs(joueurs):
        console = Console()
        table = Table(title="Liste des Joueurs")

        table.add_column("Nom", style="green")
        table.add_column("Prénom", style="green")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)

        for joueur in joueurs:
            table.add_row(joueur.nom, joueur.prenom, str(joueur.identifiant))
        console.print(table)

    @staticmethod
    def afficher_details_joueur(joueurs):
        console = Console()
        
        if joueurs:
            for joueur in joueurs:
                table = Table()
                
                table.add_column(f"Détails de {joueur.nom} {joueur.prenom}" ,style="bold cyan")
                table.add_column("Valeur", style="bold green")
                table.add_row("Date de naissance", joueur.date_naissance)
                table.add_row("Identifiant National", joueur.identifiant)

                console.print(table)

                table_tournois = Table(title="Tournois Participés", title_justify="left")
                table_tournois.add_column("Nom du tournoi", style="yellow")
                table_tournois.add_column("Points", style="magenta")
                table_tournois.add_column("Dates", style="cyan")

                for tournoi in joueur.tournois_participes:
                    dates = f"{tournoi['date_debut']} à {tournoi['date_fin']}"
                    table_tournois.add_row(tournoi["tournoi"], str(tournoi["points"]), dates)
                
                console.print(table_tournois)
                console.print("\n")
        else:
            console.print("[bold red]Joueur non trouvé.[/bold red]")
    
    @staticmethod
    def afficher_tournois(tournois):
        console = Console()

        if not tournois:
            console.print("[bold red]Aucun tournoi enregistré.[/bold red]")
            return
        table = Table(title="Liste des Tournois")

        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Lieu", style="green")
        table.add_column("Date de début", style="magenta")
        table.add_column("Date de fin", style="magenta")

        for tournoi in tournois:
            table.add_row(tournoi.nom, tournoi.lieu, tournoi.date_debut, tournoi.date_fin)
        console.print(table)



    @staticmethod
    def afficher_details_tournoi(tournoi):

        console = Console()
        details_text = Text()

        details_text.append(f"Nom : ", style="bold yellow")
        details_text.append(f"{tournoi.nom}\n", style="cyan")

        details_text.append("Lieu : ", style="bold yellow")
        details_text.append(f"{tournoi.lieu}\n", style="cyan")

        details_text.append("Date de début : ", style="bold yellow")
        details_text.append(f"{tournoi.date_debut}\n", style="cyan")

        details_text.append("Date de fin : ", style="bold yellow")
        details_text.append(f"{tournoi.date_fin}\n", style="cyan")

        details_text.append("Nombre de tours : ", style="bold yellow")
        details_text.append(f"{tournoi.nombre_tours}\n", style="cyan")

        details_text.append("Tour courant : ", style="bold yellow")
        details_text.append(f"{tournoi.tour_actuel}\n", style="cyan")

        details_text.append("Description : ", style="bold yellow")
        details_text.append(f"{tournoi.description}", style="cyan")

        panel = Panel.fit(
            details_text,
            title=f"[bold green]Détails du Tournoi - {tournoi.nom}[/bold green]",
            border_style="bright_blue",
            box=box.ROUNDED,
            padding=(1, 2),
        )
        console.print(panel)
        Rapport.liste_joueurs(tournoi.joueurs)

    @staticmethod
    def afficher_message(message):
        print(message)

    @staticmethod
    def afficher_classement(tournoi):
        console = Console()
        titre_classement = Text(f"Classement du Tournoi - {tournoi.nom}", style="bold green", justify="center")
        
        table_classement = Table(box=box.MINIMAL, expand=True)
        table_classement.add_column("Position", style="bold magenta", justify="center")
        table_classement.add_column("Joueur", style="bold yellow", justify="center")
        table_classement.add_column("Score", style="bold cyan", justify="center")

        classement = sorted(tournoi.joueurs, key=lambda j: tournoi.scores.get(j.identifiant, 0), reverse=True)
        for index, joueur in enumerate(classement, start=1):
            score = tournoi.scores.get(joueur.identifiant, 0)
            table_classement.add_row(
                f"{index}",
                f"{joueur.prenom} {joueur.nom}",
                f"{score}"
            )
        panel_classement = Panel.fit(
            table_classement,
            title=titre_classement,
            border_style="bright_blue",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        console.print(panel_classement)
    
    @staticmethod
    def afficher_tours_et_matchs(tournoi):
        console = Console()

        if not tournoi.tours:
            console.print("Aucun tour n'a été enregistré pour ce tournoi.", style="bold red")
            return
        titre_tournoi = Text(f"Tours du Tournoi - {tournoi.nom}", style="bold green", justify="center")
        console.print(Panel.fit(titre_tournoi, border_style="bright_blue", box=box.DOUBLE))

        for tour in tournoi.tours:
            titre_tour = Text(f"Tour {tour.numero}", style="bold magenta", justify="center")

            if not tour.matchs:
                console.print(Panel(f"Aucun match enregistré pour ce tour.", title=titre_tour, border_style="red", box=box.ROUNDED))
            else:
                # Créer une table pour les matchs du tour
                table_matchs = Table(box=box.MINIMAL, expand=True)
                table_matchs.add_column("Match", style="bold cyan", justify="center")
                table_matchs.add_column("Joueur 1", style="yellow", justify="center")
                table_matchs.add_column("Joueur 2", style="yellow", justify="center")
                table_matchs.add_column("Score", style="bold green", justify="center")

                for i, match in enumerate(tour.matchs, start=1):
                    joueur1 = match.joueur1
                    joueur2 = match.joueur2
                    score_joueur1, score_joueur2 = match.score
                    score_affiche = f"{score_joueur1} - {score_joueur2}" if score_joueur1 is not None and score_joueur2 is not None else "Non enregistré"

                    table_matchs.add_row(
                        f"Match {i}",
                        f"{joueur1.prenom} {joueur1.nom}",
                        f"{joueur2.prenom} {joueur2.nom}",
                        score_affiche
                    )
                panel_tour = Panel.fit(
                    table_matchs,
                    title=titre_tour,
                    border_style="bright_blue",
                    box=box.ROUNDED,
                    padding=(1, 2)
                )
                console.print(panel_tour)