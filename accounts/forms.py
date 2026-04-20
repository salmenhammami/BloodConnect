from django import forms
from django.contrib.auth.models import User
from index.models import Donneur, Hopital

class DonneurRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Donneur
        fields = ["groupe_sanguin", "sexe", "date_naissance", "ville"]

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )

        donneur = Donneur.objects.create(
            user=user,
            groupe_sanguin=self.cleaned_data["groupe_sanguin"],
            sexe=self.cleaned_data["sexe"],
            date_naissance=self.cleaned_data["date_naissance"],
            ville=self.cleaned_data["ville"],
        )

        return user


class HopitalRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Hopital
        fields = ["nom", "adresse", "ville", "agrement"]

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )

        Hopital.objects.create(
            user=user,
            nom=self.cleaned_data["nom"],
            adresse=self.cleaned_data["adresse"],
            ville=self.cleaned_data["ville"],
            agrement=self.cleaned_data["agrement"],
        )

        return user
