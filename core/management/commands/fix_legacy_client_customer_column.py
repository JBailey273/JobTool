from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """Drop legacy customer_id column from core_client if it exists."""

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'core_client'
                  AND column_name = 'customer_id'
                """
            )
            exists = cursor.fetchone() is not None
            if not exists:
                self.stdout.write(self.style.SUCCESS(
                    "No legacy column found: core_client.customer_id"
                ))
                return

            self.stdout.write("Dropping legacy column core_client.customer_id …")
            cursor.execute(
                "ALTER TABLE core_client DROP COLUMN IF EXISTS customer_id CASCADE;"
            )

        self.stdout.write(self.style.SUCCESS(
            "Dropped legacy column. You can now add Clients."
        ))
