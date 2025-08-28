# core/admin.py
from __future__ import annotations
from django.contrib import admin
from . import models

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "material_markup_percent", "is_active")
    list_filter = ("client", "is_active")
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

# .editorconfig (create this at repo root; ensures spaces-only + LF)
# NOTE: put the following content into a new file named `.editorconfig` at the repo root:
#
# root = true
#
# [*]
# end_of_line = lf
# insert_final_newline = true
# charset = utf-8
# indent_style = space
# indent_size = 4
#
# [*.{yml,yaml}]
# indent_size = 2
#
# .gitattributes (optional but recommended; normalize newlines in git)
# Create a `.gitattributes` at repo root with at least:
#
# *.py text eol=lf
# *.sh text eol=lf
# *.html text eol=lf
# *.css text eol=lf
# *.json text eol=lf
# *.yml text eol=lf
