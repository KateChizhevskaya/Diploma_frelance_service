# Generated by Django 3.1.4 on 2020-12-15 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_auto_20201208_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='masteruser',
            name='is_master',
            field=models.BooleanField(default=True),
        ),
    ]
