import csv
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count, Q
from .models import Donneur, Hopital, DemandeUrgente, Campagne, ReponseAppel, Inscription, Don
from .forms import DemandeUrgenteForm, CampagneForm, DonneurProfileForm


def index(request):
    return render(request, "index/index.html")


@login_required
def dashboard_admin(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("index")

    donneurs = Donneur.objects.all()
    hopitaux = Hopital.objects.all()
    demandes_actives = DemandeUrgente.objects.filter(statut="Active")
    total_dons = Don.objects.filter(valide=True).count()
    campagnes = Campagne.objects.all()

    stats_groupes = (
        DemandeUrgente.objects.filter(statut="Active")
        .values("groupe_sanguin")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    if request.method == "POST":
        hopital_id = request.POST.get("hopital_id")
        action = request.POST.get("action")
        if hopital_id and action == "valider":
            hopital = get_object_or_404(Hopital, id=hopital_id)
            hopital.valide = True
            hopital.save()
            messages.success(request, f"L'hôpital {hopital.nom} a été validé avec succès.")
            return redirect("dashboard_admin")

    context = {
        "donneurs": donneurs,
        "hopitaux": hopitaux,
        "demandes_actives": demandes_actives,
        "total_dons": total_dons,
        "campagnes": campagnes,
        "stats_groupes": stats_groupes,
    }
    return render(request, "index/dashboard_admin.html", context)


@login_required
def export_donneurs_csv(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("index")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="donneurs_bloodconnect.csv"'
    response.write("\ufeff")

    writer = csv.writer(response, delimiter=";")
    writer.writerow(["Nom d'utilisateur", "Email", "Nom complet", "Groupe sanguin", "Sexe", "Date de naissance", "Ville", "Points", "Niveau", "Actif", "Nombre de dons"])

    for donneur in Donneur.objects.select_related("user").all():
        writer.writerow([
            donneur.user.username,
            donneur.user.email,
            donneur.user.get_full_name(),
            donneur.groupe_sanguin,
            donneur.get_sexe_display(),
            donneur.date_naissance.strftime("%d/%m/%Y"),
            donneur.ville,
            donneur.points,
            donneur.niveau,
            "Oui" if donneur.actif else "Non",
            donneur.don_set.filter(valide=True).count(),
        ])

    return response


@login_required
def dashboard_donneur(request):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    demandes = DemandeUrgente.objects.filter(statut="Active")
    points = donneur.points
    niveau = donneur.niveau
    est_eligible = donneur.est_eligible()
    prochaine_date = donneur.prochaine_date_don()

    reponses_donneur = list(
        ReponseAppel.objects.filter(donneur=donneur).values_list("demande_id", flat=True)
    )

    inscriptions = Inscription.objects.filter(donneur=donneur).select_related("campagne")

    context = {
        "donneur": donneur,
        "points": points,
        "niveau": niveau,
        "est_eligible": est_eligible,
        "prochaine_date": prochaine_date,
        "demandes": demandes,
        "reponses_donneur": reponses_donneur,
        "inscriptions": inscriptions,
    }
    return render(request, "index/dashboard_donneur.html", context)


@login_required
def profil_donneur(request):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    if request.method == "POST":
        form = DonneurProfileForm(request.POST, instance=donneur)
        if form.is_valid():
            form.save()
            request.user.first_name = request.POST.get("first_name", "")
            request.user.last_name = request.POST.get("last_name", "")
            request.user.email = request.POST.get("email", "")
            request.user.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("dashboard_donneur")
    else:
        form = DonneurProfileForm(instance=donneur)

    return render(request, "index/profil_donneur.html", {"form": form, "donneur": donneur})


@login_required
def toggle_actif(request):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    donneur.actif = not donneur.actif
    donneur.save()

    if donneur.actif:
        messages.success(request, "Votre compte est de nouveau actif. Vous recevrez les alertes d'urgence.")
    else:
        messages.info(request, "Votre compte est désactivé temporairement. Vous ne recevrez plus d'alertes.")

    return redirect("dashboard_donneur")


@login_required
def enregistrer_don(request):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    if request.method == "POST":
        date_don_str = request.POST.get("date_don")
        hopital_id = request.POST.get("hopital_id")
        notes = request.POST.get("notes", "")

        try:
            date_don = datetime.date.fromisoformat(date_don_str)
        except:
            messages.error(request, "Date invalide.")
            return redirect("dashboard_donneur")

        hopital = None
        if hopital_id:
            hopital = Hopital.objects.filter(id=hopital_id).first()

        Don.objects.create(
            donneur=donneur,
            hopital=hopital,
            date_don=date_don,
            notes=notes,
            valide=True,
        )
        donneur.points += 100
        donneur.save()
        messages.success(request, "Don enregistré avec succès ! +100 points 🎉")
        return redirect("dashboard_donneur")

    hopitaux = Hopital.objects.filter(valide=True)
    return render(request, "index/enregistrer_don.html", {"hopitaux": hopitaux})


@login_required
def dashboard_hopital(request):
    try:
        hopital = request.user.hopital
    except:
        return redirect("index")

    demandes_actives = DemandeUrgente.objects.filter(hopital=hopital, statut="Active")
    demandes_cloturees = DemandeUrgente.objects.filter(hopital=hopital, statut="Clôturée")
    campagnes = Campagne.objects.filter(hopital=hopital)

    context = {
        "hopital": hopital,
        "demandes_actives": demandes_actives,
        "demandes_cloturees": demandes_cloturees,
        "campagnes": campagnes,
    }
    return render(request, "index/dashboard_hopital.html", context)


@login_required
def create_demande(request):
    try:
        hopital = request.user.hopital
    except:
        return redirect("index")

    if not hopital.valide:
        messages.error(request, "Votre compte doit être validé par un administrateur pour publier une demande.")
        return redirect("dashboard_hopital")

    if request.method == "POST":
        form = DemandeUrgenteForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.hopital = hopital
            demande.save()
            messages.success(request, "Demande urgente publiée avec succès.")
            return redirect("dashboard_hopital")
    else:
        form = DemandeUrgenteForm()

    return render(request, "index/create_demande.html", {"form": form})


@login_required
def edit_demande(request, demande_id):
    try:
        hopital = request.user.hopital
    except:
        return redirect("index")

    demande = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)

    if request.method == "POST":
        form = DemandeUrgenteForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            messages.success(request, "Demande modifiée avec succès.")
            return redirect("dashboard_hopital")
    else:
        form = DemandeUrgenteForm(instance=demande)

    return render(request, "index/edit_demande.html", {"form": form, "demande": demande})


@login_required
def close_demande(request, demande_id):
    try:
        hopital = request.user.hopital
    except:
        return redirect("index")

    demande = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)
    demande.statut = "Clôturée"
    demande.save()
    messages.success(request, f"La demande {demande.groupe_sanguin} a été clôturée.")
    return redirect("dashboard_hopital")


@login_required
def repondre_demande(request, demande_id):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    demande = get_object_or_404(DemandeUrgente, id=demande_id)

    if not donneur.est_eligible():
        messages.error(request, "Vous n'êtes pas encore éligible pour faire un don.")
        return redirect("dashboard_donneur")

    if ReponseAppel.objects.filter(demande=demande, donneur=donneur).exists():
        messages.warning(request, "Vous avez déjà répondu à cette demande.")
    else:
        ReponseAppel.objects.create(demande=demande, donneur=donneur)
        donneur.points += 25
        donneur.save()
        messages.success(request, "Merci ! Votre intention de don a été transmise à l'hôpital. +25 points 🎉")

    return redirect("dashboard_donneur")


@login_required
def create_campagne(request):
    try:
        hopital = request.user.hopital
    except:
        return redirect("index")

    if not hopital.valide:
        messages.error(request, "Votre compte doit être validé par un administrateur pour créer une campagne.")
        return redirect("dashboard_hopital")

    if request.method == "POST":
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne = form.save(commit=False)
            campagne.hopital = hopital
            campagne.save()
            messages.success(request, "Campagne de collecte créée avec succès.")
            return redirect("dashboard_hopital")
    else:
        form = CampagneForm()

    return render(request, "index/create_campagne.html", {"form": form})


@login_required
def list_campagnes(request):
    campagnes = Campagne.objects.all().order_by("date")
    try:
        donneur = request.user.donneur
        inscriptions_ids = list(
            Inscription.objects.filter(donneur=donneur).values_list("campagne_id", flat=True)
        )
    except:
        inscriptions_ids = []

    return render(request, "index/list_campagnes.html", {
        "campagnes": campagnes,
        "inscriptions_ids": inscriptions_ids,
    })


@login_required
def inscrire_campagne(request, campagne_id):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    campagne = get_object_or_404(Campagne, id=campagne_id)

    if not donneur.est_eligible():
        messages.error(request, "Vous n'êtes pas encore éligible pour faire un don.")
        return redirect("list_campagnes")

    if Inscription.objects.filter(campagne=campagne, donneur=donneur).exists():
        messages.warning(request, "Vous êtes déjà inscrit à cette campagne.")
    else:
        nb_inscrits = Inscription.objects.filter(campagne=campagne).count()
        if nb_inscrits >= campagne.capacite_totale:
            messages.error(request, "Cette campagne est complète, plus de créneaux disponibles.")
            return redirect("list_campagnes")

        creneau_str = request.POST.get("creneau", "09:00")
        try:
            h, m = map(int, creneau_str.split(":"))
            creneau = datetime.time(h, m)
        except:
            creneau = datetime.time(9, 0)

        Inscription.objects.create(campagne=campagne, donneur=donneur, creneau_horaire=creneau)
        donneur.points += 50
        donneur.save()
        messages.success(
            request,
            f"Inscription confirmée pour la campagne {campagne.nom} à {creneau.strftime('%H:%M')}. +50 points 🎉",
        )

    return redirect("list_campagnes")
