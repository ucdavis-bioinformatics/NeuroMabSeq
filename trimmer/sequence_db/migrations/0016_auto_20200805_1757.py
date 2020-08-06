# Generated by Django 3.0.2 on 2020-08-05 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence_db', '0015_faq'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filesprocessed',
            old_name='message',
            new_name='filename',
        ),
        migrations.AddField(
            model_name='faq',
            name='is_definition',
            field=models.BooleanField(default=False),
        ),
    ]
