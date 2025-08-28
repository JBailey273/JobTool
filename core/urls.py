from __future__ import annotations
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = "core"


urlpatterns = [
path("", views.dashboard, name="dashboard"),
path("work/new/", views.add_work_entry, name="add_work"),
path("materials/new/", views.add_material_entry, name="add_material"),
path("payments/new/", views.add_payment, name="add_payment"),
path("report/<int:project_id>/", views.report, name="report"),


# Auth
path("login/", views.BrandedLoginView.as_view(), name="login"),
path("logout/", LogoutView.as_view(), name="logout"),
]
