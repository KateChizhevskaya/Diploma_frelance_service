# Generated by Django 3.1.4 on 2021-01-05 09:36

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_auto_20210105_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='defendant_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Contact phone number', max_length=128, null=True, region='BY'),
        ),
    ]
