from django.contrib import admin
from .models import Matiere, Mentor, Disponibilite


class DisponibiliteInline(admin.TabularInline):
    model = Disponibilite
    extra = 1


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("nom", "filiere", "niveau", "format_mentorat")
    filter_horizontal = ("matieres",)
    inlines = [DisponibiliteInline]


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    search_fields = ("nom",)


@admin.register(Disponibilite)
class DisponibiliteAdmin(admin.ModelAdmin):
    list_display = ("mentor", "jour", "heure_debut", "heure_fin")
