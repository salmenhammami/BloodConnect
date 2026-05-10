from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("admin/export-donneurs/", views.export_donneurs_csv, name="export_donneurs_csv"),
    path("dashboard/donneur/", views.dashboard_donneur, name="dashboard_donneur"),
    path("profil/donneur/", views.profil_donneur, name="profil_donneur"),
    path("donneur/toggle-actif/", views.toggle_actif, name="toggle_actif"),
    path("donneur/enregistrer-don/", views.enregistrer_don, name="enregistrer_don"),
    path("dashboard/hopital/", views.dashboard_hopital, name="dashboard_hopital"),
    path("demande/nouvelle/", views.create_demande, name="create_demande"),
    path("demande/<int:demande_id>/modifier/", views.edit_demande, name="edit_demande"),
    path("demande/<int:demande_id>/cloturer/", views.close_demande, name="close_demande"),
    path("demande/<int:demande_id>/repondre/", views.repondre_demande, name="repondre_demande"),
    path("campagne/nouvelle/", views.create_campagne, name="create_campagne"),
    path("campagnes/", views.list_campagnes, name="list_campagnes"),
    path("campagne/<int:campagne_id>/inscrire/", views.inscrire_campagne, name="inscrire_campagne"),
]
