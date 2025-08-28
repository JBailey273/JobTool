from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_drop_legacy_customer_columns"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                # add client_id if missing
                "ALTER TABLE IF EXISTS core_asset ADD COLUMN IF NOT EXISTS client_id integer;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                # add FK if not present (safe to re-run)
                "DO $$
"
                "BEGIN
"
                "  IF NOT EXISTS (
"
                "    SELECT 1 FROM information_schema.table_constraints
"
                "    WHERE table_name='core_asset' AND constraint_name='core_asset_client_id_fk'
"
                "  ) THEN
"
                "    ALTER TABLE core_asset
"
                "      ADD CONSTRAINT core_asset_client_id_fk
"
                "      FOREIGN KEY (client_id) REFERENCES core_client(id)
"
                "      DEFERRABLE INITIALLY DEFERRED;
"
                "  END IF;
"
                "END$$;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                "CREATE INDEX IF NOT EXISTS core_asset_client_id_idx ON core_asset (client_id);"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
