from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/donneur/", views.dashboard_donneur, name="dashboard_donneur"),
    path("dashboard/hopital/", views.dashboard_hopital, name="dashboard_hopital"),
    path("demande/nouvelle/", views.create_demande, name="create_demande"),
    path("demande/<int:demande_id>/repondre/", views.repondre_demande, name="repondre_demande"),
    path("campagne/nouvelle/", views.create_campagne, name="create_campagne"),
    path("campagnes/", views.list_campagnes, name="list_campagnes"),
    path("campagne/<int:campagne_id>/inscrire/", views.inscrire_campagne, name="inscrire_campagne"),
]
