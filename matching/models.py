from django.db import models


class Matiere(models.Model):
    """Une matière / compétence proposée par un mentor (ex: Django, Algorithmique...)."""
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Mentor(models.Model):
    FILIERE_CHOICES = [
        ("IA", "Intelligence Artificielle"),
        ("IM", "Ingénierie Mathématique"),
        ("GL", "Génie Logiciel"),
        ("SE_IOT", "Systèmes Embarqués & IoT"),
        ("SI", "Systèmes d'Information"),
    ]
    FORMAT_CHOICES = [
        ("presentiel", "Présentiel"),
        ("en_ligne", "En ligne"),
        ("les_deux", "Présentiel & En ligne"),
    ]

    nom = models.CharField(max_length=150)
    filiere = models.CharField(max_length=10, choices=FILIERE_CHOICES)
    niveau = models.CharField(max_length=50, help_text="Ex: Licence 2, Licence 3, Master 1")
    format_mentorat = models.CharField(max_length=15, choices=FORMAT_CHOICES, default="les_deux")
    matieres = models.ManyToManyField(Matiere, related_name="mentors")

    def __str__(self):
        return self.nom


class Disponibilite(models.Model):
    """Un créneau horaire de disponibilité pour un mentor."""
    JOUR_CHOICES = [
        ("lundi", "Lundi"),
        ("mardi", "Mardi"),
        ("mercredi", "Mercredi"),
        ("jeudi", "Jeudi"),
        ("vendredi", "Vendredi"),
        ("samedi", "Samedi"),
        ("dimanche", "Dimanche"),
    ]

    mentor = models.ForeignKey(Mentor, related_name="disponibilites", on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=JOUR_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        ordering = ["jour", "heure_debut"]

    def __str__(self):
        return f"{self.mentor.nom} - {self.get_jour_display()} {self.heure_debut}-{self.heure_fin}"
