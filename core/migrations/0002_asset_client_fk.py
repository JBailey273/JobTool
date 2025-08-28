from django.db import migrations


def ensure_client_fk(apps, schema_editor):
    """Ensure legacy Asset rows have a client FK.

    The original deployment used raw SQL against PostgreSQL. SQLite, used for
    local development and tests, chokes on ``IF NOT EXISTS`` clauses. This
    migration now runs the SQL only when the database vendor is PostgreSQL and
    becomes a no-op elsewhere.
    """

    if schema_editor.connection.vendor != "postgresql":  # pragma: no cover - exercised in CI
        return

    schema_editor.execute(
        """
        ALTER TABLE IF EXISTS core_asset
        ADD COLUMN IF NOT EXISTS client_id integer;
        """
    )
    schema_editor.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.table_constraints
                WHERE table_name='core_asset' AND constraint_name='core_asset_client_id_fk'
            ) THEN
                ALTER TABLE core_asset
                    ADD CONSTRAINT core_asset_client_id_fk
                    FOREIGN KEY (client_id) REFERENCES core_client(id)
                    DEFERRABLE INITIALLY DEFERRED;
            END IF;
        END
        $$;
        """
    )
    schema_editor.execute(
        """
        CREATE INDEX IF NOT EXISTS core_asset_client_id_idx
        ON core_asset (client_id);
        """
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [migrations.RunPython(ensure_client_fk, migrations.RunPython.noop)]
