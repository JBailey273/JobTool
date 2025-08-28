from django.contrib import admin
from django.utils.html import format_html

try:
    from .models import Client, Project, ProjectTotals
except Exception:  # pragma: no cover
    Client = Project = ProjectTotals = None


def _fmt_money(value: float | int | None) -> str:
    try:
        return f"${value:,.2f}"
    except Exception:
        return "—"


def _project_balance_compute(project) -> str:
    try:
        totals = ProjectTotals.for_project(project)
        return _fmt_money(getattr(totals, "balance", None))
    except Exception:
        return "—"


def _client_balance_compute(client) -> str:
    total = 0.0
    try:
        # Sum balances of active/open projects for this client
        projects = getattr(client, "project_set", None)
        if projects is None:
            return "—"
        for p in projects.filter(active=True):
            try:
                totals = ProjectTotals.for_project(p)
                total += float(getattr(totals, "balance", 0) or 0)
            except Exception:
                continue
        return _fmt_money(total)
    except Exception:
        return "—"


def _augment_admin():
    if not (Client and Project):
        return

    # Inject balance column into Project admin
    if Project in admin.site._registry:
        inst = admin.site._registry[Project]
        # attach method on the class so admin can call it
        def balance(self, obj):  # noqa: ANN001
            return _project_balance_compute(obj)
        balance.short_description = "Balance"  # type: ignore[attr-defined]
        balance.admin_order_field = None  # type: ignore[attr-defined]
        setattr(inst.__class__, "balance", balance)
        lst = tuple(getattr(inst, "list_display", ()))
        if "balance" not in lst:
            inst.list_display = lst + ("balance",)

    # Inject balance column into Client admin
    if Client in admin.site._registry:
        inst = admin.site._registry[Client]
        def running_balance(self, obj):  # noqa: ANN001
            return _client_balance_compute(obj)
        running_balance.short_description = "Running Balance"  # type: ignore[attr-defined]
        running_balance.admin_order_field = None  # type: ignore[attr-defined]
        setattr(inst.__class__, "running_balance", running_balance)
        lst = tuple(getattr(inst, "list_display", ()))
        if "running_balance" not in lst:
            inst.list_display = lst + ("running_balance",)


try:
    _augment_admin()
except Exception:
    # Never block admin if augmentation fails
    pass
