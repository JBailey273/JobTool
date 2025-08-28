from django.contrib import admin

try:
    from .models import Asset, WorkEntry, Project, Client
except Exception:  # pragma: no cover
    Asset = WorkEntry = Project = Client = None


def _augment_asset_admin():
    if not Asset or Asset not in admin.site._registry:
        return
    inst = admin.site._registry[Asset]
    # Show client in list view
    lst = tuple(getattr(inst, "list_display", ()))
    for col in ("client", "name", "active"):
        if col not in lst:
            lst += (col,)
    inst.list_display = lst
    # Basic filters & search
    inst.list_filter = tuple(set(getattr(inst, "list_filter", ())) | {"client", "active"})
    inst.search_fields = tuple(set(getattr(inst, "search_fields", ())) | {"name"})


def _augment_workentry_admin():
    if not (WorkEntry and Asset) or WorkEntry not in admin.site._registry:
        return
    inst = admin.site._registry[WorkEntry]

    # Filter asset choices by the selected project's client
    def formfield_for_foreignkey(self, db_field, request, **kwargs):  # noqa: ANN001
        field = super(inst.__class__, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "asset":
            # Best-effort: if adding via ?project=<id> filter by that client
            from django.http import QueryDict

            qd = QueryDict(request.META.get("QUERY_STRING", ""))
            proj_id = qd.get("project")
            if proj_id:
                try:
                    proj = Project.objects.select_related("client").get(pk=proj_id)
                    field.queryset = Asset.objects.filter(client=proj.client, active=True)
                except Project.DoesNotExist:
                    pass
        return field

    setattr(inst.__class__, "formfield_for_foreignkey", formfield_for_foreignkey)


try:  # apply augmentations without breaking admin
    _augment_asset_admin()
    _augment_workentry_admin()
except Exception:
    pass
