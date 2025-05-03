# Author: Ruthura ,Sravanthi
# Date: 05-02-2025
# Description : This code stores the app level urls.

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('summarize/', views.summarize, name='summarize'),
    path('analyze_existing/<int:game_id>/', views.analyze_existing_game, name='analyze_existing')
]

