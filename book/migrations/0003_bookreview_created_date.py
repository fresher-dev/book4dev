# Generated by Django 3.2 on 2022-12-05 03:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20221205_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]