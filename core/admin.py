from __future__ import annotations
from django.contrib import admin
from . import models

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "is_active")
    list_filter = ("customer", "is_active")
    search_fields = ("name",)

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "client", "material_markup_percent", "is_active")
    list_filter = ("customer", "client", "is_active")
    search_fields = ("name",)

@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "is_labor", "unit", "default_rate", "is_active")
    list_filter = ("is_labor", "unit", "is_active")
    search_fields = ("name",)

@admin.register(models.RateOverride)
class RateOverrideAdmin(admin.ModelAdmin):
    list_display = ("project", "asset", "rate")
    list_filter = ("project", "asset")

@admin.register(models.WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "project", "asset", "quantity", "rate_used", "line_total")
    list_filter = ("project", "asset", "date")
    search_fields = ("notes",)
    autocomplete_fields = ("project", "asset")

@admin.register(models.MaterialEntry)
class MaterialEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "project", "description", "cost", "markup_percent", "sell_price")
    list_filter = ("project", "date")
    search_fields = ("description",)

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("date", "project", "amount", "reference")
    list_filter = ("project", "date")
    search_fields = ("reference",)
