from django import forms
from .models import DemandeUrgente, Campagne, Donneur


class DemandeUrgenteForm(forms.ModelForm):
    class Meta:
        model = DemandeUrgente
        fields = ["groupe_sanguin", "quantite", "delai", "description"]
        widgets = {
            "delai": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "groupe_sanguin": "Groupe sanguin recherché",
            "quantite": "Quantité (en poches)",
            "delai": "Date limite",
            "description": "Description de la demande",
        }


class CampagneForm(forms.ModelForm):
    class Meta:
        model = Campagne
        fields = ["nom", "date", "lieu", "groupes_cibles", "capacite_totale"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "nom": "Nom de la campagne",
            "date": "Date de la campagne",
            "lieu": "Lieu",
            "groupes_cibles": "Groupes sanguins ciblés",
            "capacite_totale": "Nombre de créneaux disponibles",
        }


class DonneurProfileForm(forms.ModelForm):
    class Meta:
        model = Donneur
        fields = ["groupe_sanguin", "sexe", "date_naissance", "ville"]
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "groupe_sanguin": "Groupe sanguin",
            "sexe": "Sexe",
            "date_naissance": "Date de naissance",
            "ville": "Ville",
        }
