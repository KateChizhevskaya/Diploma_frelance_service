# Generated by Django 3.1.4 on 2021-01-05 10:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0013_auto_20210105_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='date_of_creating_complaint',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]