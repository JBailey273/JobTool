from django.db import migrations, models


def ensure_client_fk(apps, schema_editor):
    """Ensure legacy Asset rows have a client FK across all backends.

    The original migration used PostgreSQL-specific SQL with ``IF NOT EXISTS``
    clauses that fail on SQLite.  Using the schema editor allows Django to
    handle the appropriate SQL for the active backend.
    """

    connection = schema_editor.connection
    table_name = "core_asset"

    with connection.cursor() as cursor:
        column_names = {
            c.name for c in connection.introspection.get_table_description(cursor, table_name)
        }

    if "client_id" in column_names:
        return

    Client = apps.get_model("core", "Client")
    Asset = apps.get_model("core", "Asset")
    field = models.ForeignKey(
        Client, null=True, blank=True, related_name="assets", on_delete=models.CASCADE
    )
    field.set_attributes_from_name("client")
    schema_editor.add_field(Asset, field)


def remove_client_fk(apps, schema_editor):
    """Reverse the ``ensure_client_fk`` operation."""

    connection = schema_editor.connection
    table_name = "core_asset"

    with connection.cursor() as cursor:
        column_names = {
            c.name for c in connection.introspection.get_table_description(cursor, table_name)
        }

    if "client_id" not in column_names:
        return

    Asset = apps.get_model("core", "Asset")
    field = Asset._meta.get_field("client")
    schema_editor.remove_field(Asset, field)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [migrations.RunPython(ensure_client_fk, remove_client_fk)]
