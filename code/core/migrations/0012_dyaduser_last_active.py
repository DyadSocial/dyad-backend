# Generated by Django 3.2.9 on 2022-01-25 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20211206_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='dyaduser',
            name='last_active',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]