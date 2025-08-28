# path: core/__init__.py
# why: ensure admin branding is applied even if we don't edit admin.py
try:  # import has side effects that set admin titles safely
    from . import admin_branding  # noqa: F401
except Exception:
    # Never block app startup if branding import fails
    pass
