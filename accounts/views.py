from django.shortcuts import render, redirect
from .forms import DonneurRegisterForm, HopitalRegisterForm
from django.contrib.auth import login, authenticate


def register_donneur(request):
    form = DonneurRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard_donneur")

    return render(request, "accounts/register_donneur.html", {"form": form})


def register_hopital(request):
    form = HopitalRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard_hopital")

    return render(request, "accounts/register_hopital.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if hasattr(user, "donneur"):
                return redirect("dashboard_donneur")
            elif hasattr(user, "hopital"):
                return redirect("dashboard_hopital")
            else:
                return redirect("admin:index")

    return render(request, "accounts/login.html")
