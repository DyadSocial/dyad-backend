# Generated by Django 3.2.9 on 2021-12-06 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_dyaduser_dyad_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dyaduser',
            name='Dyad_Group',
        ),
    ]
