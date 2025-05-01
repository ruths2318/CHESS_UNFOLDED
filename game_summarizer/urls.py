from django.urls import path

from . import views
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('summarize/', views.summarize, name='summarize'),
    path('analyze_existing/<int:game_id>/', views.analyze_existing_game, name='analyze_existing'),
    path("game/<int:game_id>/analyze/", views.analyze_existing_game, name="analyze_existing_game"),
]


