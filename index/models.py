from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User

# Choix réutilisables
GROUPES_SANGUINS = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]


class Donneur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    sexe = models.CharField(max_length=1, choices=[("M", "Homme"), ("F", "Femme")])
    date_naissance = models.DateField()
    ville = models.CharField(max_length=100)
    actif = models.BooleanField(default=True)
    points = models.PositiveIntegerField(default=0)

    @property
    def niveau(self):
        if self.points >= 1000: return "Sauveur d'Or"
        if self.points >= 500: return "Héros d'Argent"
        if self.points >= 100: return "Goutte de Bronze"
        return "Nouveau Donneur"

    def prochaine_date_don(self):
        dernier_don = self.don_set.filter(valide=True).order_by('-date_don').first()
        if not dernier_don:
            return date.today()
        delai = timedelta(days=56) if self.sexe == 'M' else timedelta(days=84)
        return dernier_don.date_don + delai

    def est_eligible(self):
        return date.today() >= self.prochaine_date_don()

    def __str__(self):
        return f"Donneur: {self.user.get_full_name()} ({self.groupe_sanguin})"


class Hopital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    agrement = models.CharField(max_length=100, unique=True)
    valide = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Hôpital: {self.nom}"


class DemandeUrgente(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES_SANGUINS)
    quantite = models.PositiveIntegerField(help_text="Quantité en poches")
    delai = models.DateTimeField()
    statut = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Clôturée", "Clôturée")],
        default="Active",
    )
    description = models.TextField()

    def __str__(self):
        return f"Urgence {self.groupe_sanguin} - {self.hopital.nom}"


class Don(models.Model):
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.SET_NULL, null=True)
    date_don = models.DateField()
    notes = models.TextField(blank=True, null=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"Don de {self.donneur.user.username} le {self.date_don}"


class Campagne(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    date = models.DateField()
    lieu = models.CharField(max_length=200)
    groupes_cibles = models.CharField(max_length=100, help_text="Ex: O-, A+, B-")
    capacite_totale = models.PositiveIntegerField()

    def __str__(self):
        return f"Campagne {self.nom} - {self.date}"


class Inscription(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    creneau_horaire = models.TimeField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donneur.user.username} inscrit à {self.campagne.nom}"


class ReponseAppel(models.Model):
    demande = models.ForeignKey(DemandeUrgente, on_delete=models.CASCADE)
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    date_reponse = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[("En attente", "En attente"), ("Confirmée", "Confirmée")],
        default="En attente",
    )

    def __str__(self):
        return f"Réponse de {self.donneur.user.username} pour urgence {self.demande.id}"
