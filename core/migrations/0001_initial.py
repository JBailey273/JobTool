from django.db import migrations, models
('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
('rate', models.DecimalField(decimal_places=2, max_digits=12)),
('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_overrides', to='core.asset')),
('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_overrides', to='core.project')),
],
options={'unique_together': {('project', 'asset')}},
),
migrations.CreateModel(
name='WorkEntry',
fields=[
('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
('date', models.DateField(default=django.utils.timezone.now)),
('quantity', models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0.00'))),
('notes', models.TextField(blank=True)),
('rate_used', models.DecimalField(decimal_places=2, editable=False, max_digits=12, default=Decimal('0.00'))),
('line_total', models.DecimalField(decimal_places=2, editable=False, max_digits=12, default=Decimal('0.00'))),
('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.asset')),
('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_entries', to='core.project')),
],
),
migrations.CreateModel(
name='MaterialEntry',
fields=[
('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
('date', models.DateField(default=django.utils.timezone.now)),
('description', models.CharField(max_length=255)),
('cost', models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0.00'))),
('markup_percent', models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)),
('sell_price', models.DecimalField(decimal_places=2, editable=False, max_digits=12, default=Decimal('0.00'))),
('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_entries', to='core.project')),
],
),
migrations.CreateModel(
name='Payment',
fields=[
('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
('date', models.DateField(default=django.utils.timezone.now)),
('amount', models.DecimalField(decimal_places=2, max_digits=12)),
('reference', models.CharField(max_length=200, blank=True)),
('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='core.project')),
],
),
]
