# Generated by Django 4.2.7 on 2023-11-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='manage',
            new_name='manager',
        ),
        migrations.AlterField(
            model_name='event',
            name='even_date',
            field=models.DateField(verbose_name='Event Date'),
        ),
    ]
