# Generated by Django 4.2.7 on 2023-12-05 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_venue_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
