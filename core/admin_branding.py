# path: core/admin_branding.py
# why: apply admin branding without touching your existing admin.py
from django.contrib import admin

admin.site.site_header = "Squire Enterprises — Admin"
admin.site.site_title = "Squire Enterprises Admin"
admin.site.index_title = "Administration"
