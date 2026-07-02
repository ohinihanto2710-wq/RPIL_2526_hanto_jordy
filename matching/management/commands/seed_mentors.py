from datetime import time

from django.core.management.base import BaseCommand

from matching.models import Matiere, Mentor, Disponibilite


class Command(BaseCommand):
    help = "Pré-remplit la base de données avec des mentors de démonstration."

    def handle(self, *args, **options):
        Disponibilite.objects.all().delete()
        Mentor.objects.all().delete()
        Matiere.objects.all().delete()

        def get_matieres(*noms):
            return [Matiere.objects.get_or_create(nom=nom)[0] for nom in noms]

        mentors_data = [
            {
                "nom": "Rachidatou ALAO",
                "filiere": "GL",
                "niveau": "Licence 3",
                "format_mentorat": "les_deux",
                "matieres": ["Django", "Python", "Bases de données"],
                "disponibilites": [
                    ("lundi", time(14, 0), time(17, 0)),
                    ("mercredi", time(9, 0), time(12, 0)),
                ],
            },
            {
                "nom": "Enagnon KPOSSOU",
                "filiere": "IA",
                "niveau": "Master 1",
                "format_mentorat": "en_ligne",
                "matieres": ["Machine Learning", "Python", "Mathématiques"],
                "disponibilites": [
                    ("mardi", time(16, 0), time(19, 0)),
                    ("samedi", time(10, 0), time(13, 0)),
                ],
            },
            {
                "nom": "Nadège HOUNKPATIN",
                "filiere": "SI",
                "niveau": "Licence 2",
                "format_mentorat": "presentiel",
                "matieres": ["Bases de données", "Algorithmique", "UML"],
                "disponibilites": [
                    ("jeudi", time(8, 0), time(11, 0)),
                    ("vendredi", time(15, 0), time(18, 0)),
                ],
            },
            {
                "nom": "Israël DOSSOU-YOVO",
                "filiere": "SE_IOT",
                "niveau": "Licence 3",
                "format_mentorat": "les_deux",
                "matieres": ["C", "Systèmes embarqués", "Algorithmique"],
                "disponibilites": [
                    ("lundi", time(9, 0), time(12, 0)),
                    ("dimanche", time(14, 0), time(16, 0)),
                ],
            },
            {
                "nom": "Chimène AGOSSOU",
                "filiere": "IM",
                "niveau": "Master 1",
                "format_mentorat": "en_ligne",
                "matieres": ["Mathématiques", "Recherche opérationnelle", "Python"],
                "disponibilites": [
                    ("mercredi", time(17, 0), time(20, 0)),
                ],
            },
        ]

        for data in mentors_data:
            mentor = Mentor.objects.create(
                nom=data["nom"],
                filiere=data["filiere"],
                niveau=data["niveau"],
                format_mentorat=data["format_mentorat"],
            )
            mentor.matieres.set(get_matieres(*data["matieres"]))
            for jour, debut, fin in data["disponibilites"]:
                Disponibilite.objects.create(mentor=mentor, jour=jour, heure_debut=debut, heure_fin=fin)

        self.stdout.write(self.style.SUCCESS(f"{len(mentors_data)} mentors créés avec succès."))
