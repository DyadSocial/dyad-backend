# Generated by Django 3.2.9 on 2021-12-06 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_dyadgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyaduser',
            name='Dyad_Group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.dyadgroup'),
            preserve_default=False,
        ),
    ]
