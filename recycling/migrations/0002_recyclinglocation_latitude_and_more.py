# Generated by Django 5.2.1 on 2025-06-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recyclinglocation',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=-4.567218952605757, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recyclinglocation',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=-37.79155341109657, max_digits=9),
            preserve_default=False,
        ),
    ]
