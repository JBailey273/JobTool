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
        # If you still have a core_customer table and want it gone, uncomment below.
        # migrations.RunSQL(
        #     sql=("DROP TABLE IF EXISTS core_customer CASCADE;"),
        #     reverse_sql=migrations.RunSQL.noop,
        # ),
    ]
