from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_client "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
