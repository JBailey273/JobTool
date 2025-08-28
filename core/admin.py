from __future__ import annotations

from django.contrib import admin

from .models import Asset, Client, MaterialEntry, Payment, Project, RateOverride, WorkEntry


# ---------- Client ----------
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name",)


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
    list_display = ("client", "name", "active")
    list_filter = ("client", "active")
    search_fields = ("name", "location", "client__name")
    autocomplete_fields = ("client",)
    list_select_related = ("client",)


# ---------- Work Entry ----------
@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    list_display = ("project", "date", "hours", "asset")
    list_filter = ("project", "asset")
    date_hierarchy = "date"
    autocomplete_fields = ("project", "asset")
    list_select_related = ("project", "asset", "project__client")


# ---------- Material Entry ----------
@admin.register(MaterialEntry)
class MaterialEntryAdmin(admin.ModelAdmin):
    list_display = ("project", "date", "description", "quantity", "unit_cost")
    list_filter = ("project",)
    date_hierarchy = "date"
    autocomplete_fields = ("project",)
    list_select_related = ("project",)


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


# Branding (optional; safe to keep)
admin.site.site_header = "Squire Enterprises — Admin"
admin.site.site_title = "Squire Enterprises Admin"
admin.site.index_title = "Administration"
