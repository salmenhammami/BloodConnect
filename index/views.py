from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Donneur, Hopital, DemandeUrgente, Campagne, ReponseAppel, Inscription
from .forms import DemandeUrgenteForm, CampagneForm

def index(request):
    return render(request, "index/index.html")

@login_required
def dashboard_admin(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("index")
        
    donneurs = Donneur.objects.all()
    hopitaux = Hopital.objects.all()
    demandes = DemandeUrgente.objects.all()
    
    if request.method == "POST":
        # Handle hospital validation
        hopital_id = request.POST.get("hopital_id")
        action = request.POST.get("action")
        if hopital_id and action == "valider":
            hopital = get_object_or_404(Hopital, id=hopital_id)
            hopital.valide = True
            hopital.save()
            messages.success(request, f"L'hôpital {hopital.nom} a été validé avec succès.")
            return redirect("dashboard_admin")
            
    context = {
        'donneurs': donneurs,
        'hopitaux': hopitaux,
        'demandes': demandes,
    }
    return render(request, "index/dashboard_admin.html", context)

@login_required
def dashboard_donneur(request):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")
    
    # Get active urgent requests compatible with donor's blood type (simplification: exact match or O-)
    demandes = DemandeUrgente.objects.filter(statut="Active")
    # Gamification
    points = donneur.points
    niveau = donneur.niveau
    est_eligible = donneur.est_eligible()
    prochaine_date = donneur.prochaine_date_don()
    
    context = {
        'donneur': donneur,
        'points': points,
        'niveau': niveau,
        'est_eligible': est_eligible,
        'prochaine_date': prochaine_date,
        'demandes': demandes
    }
    return render(request, "index/dashboard_donneur.html", context)

@login_required
def dashboard_hopital(request):
    try:
        hopital = request.user.hopital
    except:
        return redirect("index")
        
    demandes = DemandeUrgente.objects.filter(hopital=hopital)
    campagnes = Campagne.objects.filter(hopital=hopital)
    
    context = {
        'hopital': hopital,
        'demandes': demandes,
        'campagnes': campagnes
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
def repondre_demande(request, demande_id):
    try:
        donneur = request.user.donneur
    except:
        return redirect("index")

    demande = get_object_or_404(DemandeUrgente, id=demande_id)

    if not donneur.est_eligible():
        messages.error(request, "Vous n'êtes pas encore éligible pour faire un don.")
        return redirect("dashboard_donneur")

    # Ensure no duplicate active response
    if ReponseAppel.objects.filter(demande=demande, donneur=donneur).exists():
        messages.warning(request, "Vous avez déjà répondu à cette demande.")
    else:
        ReponseAppel.objects.create(demande=demande, donneur=donneur)
        messages.success(request, "Merci ! Votre intention de don a été transmise à l'hôpital.")

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
    campagnes = Campagne.objects.all().order_by('date')
    return render(request, "index/list_campagnes.html", {"campagnes": campagnes})

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
        import datetime
        creneau = datetime.time(9, 0) 
        Inscription.objects.create(campagne=campagne, donneur=donneur, creneau_horaire=creneau)
        messages.success(request, f"Inscription confirmée pour la campagne {campagne.nom}.")

    return redirect("list_campagnes")
