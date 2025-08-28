from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Asset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("active", models.BooleanField(default=True)),
                (
                    "client",
                    models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name="assets", to="core.client"),
                ),
            ],
            options={
                "verbose_name": "Asset",
                "verbose_name_plural": "Assets",
                "ordering": ["name"],
                "unique_together": {("client", "name")},
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("location", models.CharField(blank=True, max_length=200)),
                ("hourly_rate", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("active", models.BooleanField(default=True)),
                ("client", models.ForeignKey(on_delete=models.CASCADE, related_name="projects", to="core.client")),
            ],
            options={"verbose_name": "Job", "ordering": ["client__name", "name"]},
        ),
        migrations.AddConstraint(
            model_name="project",
            constraint=models.UniqueConstraint(fields=("client", "name"), name="uniq_project_per_client"),
        ),
        migrations.CreateModel(
            name="RateOverride",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("hourly_rate", models.DecimalField(decimal_places=2, max_digits=10)),
                ("asset", models.ForeignKey(on_delete=models.CASCADE, to="core.asset")),
                ("project", models.ForeignKey(on_delete=models.CASCADE, to="core.project")),
            ],
            options={"unique_together": {("project", "asset")}},
        ),
        migrations.CreateModel(
            name="WorkEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("hours", models.DecimalField(decimal_places=2, max_digits=7)),
                ("notes", models.TextField(blank=True)),
                ("asset", models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, to="core.asset")),
                ("project", models.ForeignKey(on_delete=models.CASCADE, related_name="work", to="core.project")),
            ],
            options={"ordering": ["-date", "id"]},
        ),
        migrations.CreateModel(
            name="MaterialEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("description", models.CharField(max_length=200)),
                ("quantity", models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ("unit_cost", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("project", models.ForeignKey(on_delete=models.CASCADE, related_name="materials", to="core.project")),
            ],
            options={"ordering": ["-date", "id"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("notes", models.TextField(blank=True)),
                ("project", models.ForeignKey(on_delete=models.CASCADE, related_name="payments", to="core.project")),
            ],
            options={"ordering": ["-date", "id"]},
        ),
    ]
