"""
Moteur de matching mentor <-> mentoré.

Critères de compatibilité (cahier des charges) :
  1. Au moins une matière/compétence en commun.
  2. Compatibilité horaire avec une tolérance de ± 1 heure.

Le score de compatibilité est calculé simplement :
  - jusqu'à 70 points selon la proportion de matières en commun,
  - jusqu'à 30 points si la filière du mentor correspond à celle recherchée
    (bonus optionnel, pas éliminatoire).
"""
from datetime import timedelta, datetime

TOLERANCE = timedelta(hours=1)


def _heure_dans_creneau(heure_souhaitee, heure_debut, heure_fin):
    """Vérifie si `heure_souhaitee` tombe dans [heure_debut - 1h, heure_fin + 1h]."""
    base = datetime(2000, 1, 1)
    h_souhaitee = datetime.combine(base, heure_souhaitee)
    h_debut = datetime.combine(base, heure_debut) - TOLERANCE
    h_fin = datetime.combine(base, heure_fin) + TOLERANCE
    return h_debut <= h_souhaitee <= h_fin


def trouver_mentors_compatibles(mentors_queryset, matieres_recherchees, heure_souhaitee, jour=None, filiere=None):
    """
    Retourne la liste des mentors compatibles, triée par score décroissant.

    mentors_queryset: QuerySet de Mentor (avec matieres et disponibilites préchargées)
    matieres_recherchees: liste de noms de matières (str), normalisés en minuscules
    heure_souhaitee: objet datetime.time
    jour: str optionnel ("lundi", ...) pour filtrer le jour de disponibilité
    filiere: str optionnel, code filière (ex: "GL") pour bonus de score
    """
    matieres_recherchees_norm = {m.strip().lower() for m in matieres_recherchees if m.strip()}
    resultats = []

    for mentor in mentors_queryset:
        matieres_mentor = {m.nom.lower(): m.nom for m in mentor.matieres.all()}
        communes = [nom_original for cle, nom_original in matieres_mentor.items() if cle in matieres_recherchees_norm]

        if not communes:
            continue  # critère 1 non rempli : aucune matière en commun

        # critère 2 : au moins un créneau compatible (± 1h), sur le jour demandé si précisé
        creneaux = mentor.disponibilites.all()
        if jour:
            creneaux = [d for d in creneaux if d.jour == jour]

        creneau_compatible = None
        for d in creneaux:
            if _heure_dans_creneau(heure_souhaitee, d.heure_debut, d.heure_fin):
                creneau_compatible = d
                break

        if not creneau_compatible:
            continue

        # calcul du score
        score_matieres = (len(communes) / len(matieres_recherchees_norm)) * 70
        score_filiere = 30 if (filiere and mentor.filiere == filiere) else 0
        score = round(score_matieres + score_filiere)

        resultats.append({
            "id": mentor.id,
            "nom": mentor.nom,
            "filiere": mentor.get_filiere_display(),
            "niveau": mentor.niveau,
            "format_mentorat": mentor.get_format_mentorat_display(),
            "matieres_communes": communes,
            "disponibilite": f"{creneau_compatible.get_jour_display()} {creneau_compatible.heure_debut.strftime('%H:%M')} - {creneau_compatible.heure_fin.strftime('%H:%M')}",
            "score": score,
        })

    resultats.sort(key=lambda r: r["score"], reverse=True)
    return resultats
