# Generated by Django 4.1.1 on 2023-03-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence_db', '0006_trimmersequence_anarci_bad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trimmersequence',
            name='bad_support',
            field=models.BooleanField(default=False),
        ),
    ]