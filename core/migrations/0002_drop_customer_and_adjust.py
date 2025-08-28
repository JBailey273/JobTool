from django.db import migrations, models


class Migration(migrations.Migration):
dependencies = [
('core', '0001_initial'),
]


operations = [
migrations.AlterUniqueTogether(
name='client',
unique_together=set(),
),
migrations.AlterUniqueTogether(
name='project',
unique_together=set(),
),
migrations.RemoveField(
model_name='client',
name='customer',
),
migrations.RemoveField(
model_name='project',
name='customer',
),
migrations.AlterField(
model_name='client',
name='name',
field=models.CharField(max_length=200, unique=True),
),
migrations.AlterUniqueTogether(
name='project',
unique_together={('client', 'name')},
),
migrations.DeleteModel(
name='Customer',
),
]
