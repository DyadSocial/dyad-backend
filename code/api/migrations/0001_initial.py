# Generated by Django 3.2.9 on 2021-12-05 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=24)),
                ('title', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=280)),
                ('date', models.DateTimeField(verbose_name='Date Created')),
                ('image', models.ImageField(blank=True, upload_to='images/%Y/%m/%d')),
            ],
        ),
    ]
