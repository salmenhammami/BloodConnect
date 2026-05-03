from django import forms
from .models import DemandeUrgente, Campagne

class DemandeUrgenteForm(forms.ModelForm):
    class Meta:
        model = DemandeUrgente
        fields = ['groupe_sanguin', 'quantite', 'delai', 'description']
        widgets = {
            'delai': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CampagneForm(forms.ModelForm):
    class Meta:
        model = Campagne
        fields = ['nom', 'date', 'lieu', 'groupes_cibles', 'capacite_totale']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
