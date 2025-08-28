"""URL patterns for core views."""

from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("healthz/", views.healthz, name="healthz"),
    path("", views.root, name="root"),
    path("login/", views.BrandedLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("work/new/", views.add_work_entry, name="work_new"),
    path("materials/new/", views.add_material_entry, name="material_new"),
    path("payments/new/", views.add_payment, name="payment_new"),
    path("report/<int:project_id>/", views.report, name="report"),
]

