from django.db import migrations


class Migration(migrations.Migration):
    # Fix: depend on your existing 0003 so the graph is linear
    dependencies = [
        ("core", "0003_remove_customer_column"),
    ]

    operations = [
        # 1) Ensure column exists
        migrations.RunSQL(
            sql="""
                ALTER TABLE IF EXISTS core_asset
                ADD COLUMN IF NOT EXISTS client_id integer;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # 2) Add FK if missing (idempotent)
        migrations.RunSQL(
            sql="""
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
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # 3) Helpful index
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS core_asset_client_id_idx
                ON core_asset (client_id);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
