# Generated by Django 4.2.7 on 2023-11-28 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rename_manage_event_manager_alter_event_even_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='even_date',
            field=models.DateTimeField(verbose_name='Event Date'),
        ),
    ]
