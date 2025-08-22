from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/<str:unique_id>/", views.dashboard, name="dashboard"),
]
