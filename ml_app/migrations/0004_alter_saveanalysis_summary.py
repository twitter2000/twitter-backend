# Generated by Django 4.0.3 on 2022-05-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_app', '0003_saveanalysis_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saveanalysis',
            name='summary',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
