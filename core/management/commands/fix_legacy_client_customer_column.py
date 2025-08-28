from django.core.management.base import BaseCommand
from django.db import connection


TABLES = [
    "core_client",
    "core_project",
    "core_asset",
    "core_workentry",
    "core_materialentry",
    "core_payment",
    "core_rateoverride",
]


class Command(BaseCommand):
    """Drop legacy customer_id column from all known tables if present."""

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            for table in TABLES:
                cursor.execute(
                    """
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = %s
                      AND column_name = 'customer_id'
                    """,
                    [table],
                )
                exists = cursor.fetchone() is not None
                if not exists:
                    self.stdout.write(self.style.NOTICE(f"{table}.customer_id: not found"))
                    continue

                self.stdout.write(f"Dropping {table}.customer_id …")
                cursor.execute(
                    f"ALTER TABLE {table} DROP COLUMN IF EXISTS customer_id CASCADE;"
                )
                self.stdout.write(self.style.SUCCESS(f"Dropped {table}.customer_id"))

        self.stdout.write(self.style.SUCCESS("Legacy customer_id cleanup complete."))
