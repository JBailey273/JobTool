# path: core/migrations/0003_remove_customer_column.py
# why: Production DB still has a NOT NULL core_client.customer_id from the old schema.
#      This drops the legacy column safely so adding Clients works again.
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_drop_customer_and_adjust"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE IF EXISTS core_client "
                "DROP COLUMN IF EXISTS customer_id CASCADE;"
            ),
            reverse_sql=migrations.RunSQL.noop,  # why: we intentionally keep the column removed
        ),
    ]
