from django.urls import path
from . import views

app_name = "matching"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/rechercher/", views.rechercher_mentors, name="rechercher"),
]
