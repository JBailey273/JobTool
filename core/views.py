"""Core application views.

Provides the dashboard, data-entry forms and project reports.
"""

from __future__ import annotations

from typing import Dict, List

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MaterialEntryForm, PaymentForm, ProjectPickerForm, WorkEntryForm
from .models import MaterialEntry, Payment, Project, ProjectTotals, WorkEntry


def healthz(_request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok", content_type="text/plain")


def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("core:dashboard")
    return redirect("core:login")


class BrandedLoginView(LoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):  # type: ignore[override]
        remember = self.request.POST.get("remember")
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProjectPickerForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data["project"]
            return redirect("core:report", project_id=project.id)
    else:
        form = ProjectPickerForm()
    return render(request, "core/dashboard.html", {"form": form})


@login_required
def add_work_entry(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            messages.success(request, "Work entry saved.")
            return redirect("core:report", project_id=entry.project_id)
    else:
        form = WorkEntryForm(initial=request.GET.dict())
    return render(request, "core/work_entry_form.html", {"form": form})


@login_required
def add_material_entry(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MaterialEntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            messages.success(request, "Material entry saved.")
            return redirect("core:report", project_id=entry.project_id)
    else:
        form = MaterialEntryForm(initial=request.GET.dict())
    return render(request, "core/material_entry_form.html", {"form": form})


@login_required
def add_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            entry = form.save()
            messages.success(request, "Payment recorded.")
            return redirect("core:report", project_id=entry.project_id)
    else:
        form = PaymentForm(initial=request.GET.dict())
    return render(request, "core/payment_form.html", {"form": form})


@login_required
def report(request: HttpRequest, project_id: int) -> HttpResponse:
    project = get_object_or_404(Project, pk=project_id)

    work_entries = (
        WorkEntry.objects.filter(project=project)
        .select_related("asset")
        .order_by("-date", "id")
    )

    raw_materials = MaterialEntry.objects.filter(project=project).order_by("-date", "id")
    material_entries: List[Dict[str, object]] = []
    for m in raw_materials:
        cost = m.total
        material_entries.append(
            {
                "date": m.date,
                "description": m.description,
                "cost": cost,
                "markup_percent": None,
                "sell_price": cost,
            }
        )

    payments = Payment.objects.filter(project=project).order_by("-date", "id")

    totals = ProjectTotals.for_project(project)
    totals_ctx = {
        "work_total": totals.labor,
        "materials_total": totals.materials,
        "payments_total": totals.payments,
        "balance_due": totals.balance,
        "grand_total": totals.labor + totals.materials,
    }

    ctx = {
        "project": project,
        "work_entries": work_entries,
        "material_entries": material_entries,
        "payments": payments,
        "totals": totals_ctx,
    }

    return render(request, "core/report.html", ctx)

