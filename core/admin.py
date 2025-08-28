from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.contrib import admin
from django.http import QueryDict

from .models import (
    Asset,
    Client,
    MaterialEntry,
    Payment,
    Project,
    ProjectTotals,
    RateOverride,
    WorkEntry,
)


# ---------- helpers ----------

def _fmt_money(value: Decimal | float | int | None) -> str:
    try:
        return f"${Decimal(value):,.2f}"
    except Exception:
        return "—"


# ---------- Client ----------

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "running_balance")
    list_filter = ("active",)
    search_fields = ("name",)

    def running_balance(self, obj: Client) -> str:  # type: ignore[override]
        total = Decimal("0")
        for p in obj.projects.filter(active=True):
            totals = ProjectTotals.for_project(p)
            total += totals.balance
        return _fmt_money(total)

    running_balance.short_description = "Running Balance"  # type: ignore[attr-defined]


# ---------- Asset (formerly Resource) ----------

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("client", "name", "active")
    list_filter = ("client", "active")
    search_fields = ("name", "client__name")
    autocomplete_fields = ("client",)
    list_select_related = ("client",)


# ---------- Project (Job) ----------

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("client", "name", "active", "balance")
    list_filter = ("client", "active")
    search_fields = ("name", "location", "client__name")
    autocomplete_fields = ("client",)
    list_select_related = ("client",)
    fieldsets = (
        (None, {"fields": ("client", "name", "location", "active")}),
        ("Rates & Dates", {"fields": ("hourly_rate", "start_date", "end_date")}),
    )

    def balance(self, obj: Project) -> str:  # type: ignore[override]
        totals = ProjectTotals.for_project(obj)
        return _fmt_money(totals.balance)

    balance.short_description = "Balance"  # type: ignore[attr-defined]


# ---------- Work Entry ----------

@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    list_display = ("project", "date", "hours", "asset")
    list_filter = ("project", "asset")
    date_hierarchy = "date"
    autocomplete_fields = ("project", "asset")
    list_select_related = ("project", "asset", "project__client")

    # Filter Asset choices to those owned by the Project's Client on add views
    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # type: ignore[override]
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "asset" and request:
            qd = QueryDict(request.META.get("QUERY_STRING", ""))
            proj_id = qd.get("project")
            if proj_id:
                try:
                    proj = Project.objects.select_related("client").get(pk=proj_id)
                    field.queryset = Asset.objects.filter(client=proj.client, active=True)
                except Project.DoesNotExist:
                    pass
        return field


# ---------- Material Entry ----------

@admin.register(MaterialEntry)
class MaterialEntryAdmin(admin.ModelAdmin):
    list_display = ("project", "date", "description", "quantity", "unit_cost", "total_amount")
    list_filter = ("project",)
    date_hierarchy = "date"
    autocomplete_fields = ("project",)
    list_select_related = ("project",)

    def total_amount(self, obj: MaterialEntry) -> str:  # type: ignore[override]
        return _fmt_money(obj.total)

    total_amount.short_description = "Total"  # type: ignore[attr-defined]


# ---------- Payment ----------

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("project", "date", "amount")
    list_filter = ("project",)
    date_hierarchy = "date"
    autocomplete_fields = ("project",)
    list_select_related = ("project",)


# ---------- Rate Override ----------

@admin.register(RateOverride)
class RateOverrideAdmin(admin.ModelAdmin):
    list_display = ("project", "asset", "hourly_rate")
    list_filter = ("project", "asset")
    autocomplete_fields = ("project", "asset")
    list_select_related = ("project", "asset")


# Optional: brand the admin titles (kept here for convenience; templates also override branding)
admin.site.site_header = "Squire Enterprises — Admin"
admin.site.site_title = "Squire Enterprises Admin"
admin.site.index_title = "Administration"
