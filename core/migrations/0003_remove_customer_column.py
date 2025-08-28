from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_drop_customer_and_adjust"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_project "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_asset "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_workentry "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_materialentry "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_payment "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_rateoverride "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
