# Generated by Django 3.0.2 on 2020-07-15 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence_db', '0013_delete_mymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesProcessed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=400)),
            ],
        ),
    ]