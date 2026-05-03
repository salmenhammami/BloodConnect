from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import DonneurRegisterForm, HopitalRegisterForm


def register_donneur(request):
    form = DonneurRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Inscription réussie. Bienvenue sur BloodConnect !")
        return redirect("dashboard_donneur")
    elif request.method == "POST":
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    return render(request, "accounts/register_donneur.html", {"form": form})


def register_hopital(request):
    form = HopitalRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Inscription réussie. En attente de validation admin.")
        return redirect("dashboard_hopital")
    elif request.method == "POST":
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    return render(request, "accounts/register_hopital.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Heureux de vous revoir, {username} !")

            if user.is_superuser or user.is_staff:
                return redirect("dashboard_admin")
            elif hasattr(user, "donneur"):
                return redirect("dashboard_donneur")
            elif hasattr(user, "hopital"):
                return redirect("dashboard_hopital")
            else:
                return redirect("index")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("index")
