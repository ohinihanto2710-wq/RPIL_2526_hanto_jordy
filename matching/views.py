import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import Mentor, Matiere
from .services import trouver_mentors_compatibles


@require_GET
def index(request):
    """Page unique : formulaire de recherche de mentor."""
    matieres = Matiere.objects.all()
    return render(request, "matching/index.html", {"matieres": matieres})


# Protection CSRF standard de Django : le token est fourni par {% csrf_token %}
# dans le template et renvoyé via l'en-tête X-CSRFToken en JS (voir main.js).
@require_POST
def rechercher_mentors(request):
    """
    Endpoint JSON de matching.
    Attend un body JSON : { matieres: [...], heure: "14:30", jour: "lundi" (optionnel), filiere: "GL" (optionnel) }
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"erreur": "Requête invalide."}, status=400)

    matieres = data.get("matieres") or []
    heure_str = data.get("heure")
    jour = data.get("jour") or None
    filiere = data.get("filiere") or None

    if not matieres:
        return JsonResponse({"erreur": "Veuillez indiquer au moins une matière ou compétence."}, status=400)

    if not heure_str:
        return JsonResponse({"erreur": "Veuillez indiquer une heure souhaitée."}, status=400)

    try:
        heure_souhaitee = datetime.strptime(heure_str, "%H:%M").time()
    except ValueError:
        return JsonResponse({"erreur": "Format d'heure invalide (attendu HH:MM)."}, status=400)

    mentors_qs = Mentor.objects.prefetch_related("matieres", "disponibilites").all()

    resultats = trouver_mentors_compatibles(
        mentors_qs,
        matieres_recherchees=matieres,
        heure_souhaitee=heure_souhaitee,
        jour=jour,
        filiere=filiere,
    )

    return JsonResponse({"resultats": resultats, "count": len(resultats)})
