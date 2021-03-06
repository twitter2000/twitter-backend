# Generated by Django 4.0.3 on 2022-05-14 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('saved_date', models.DateTimeField(auto_now_add=True)),
                ('saved_data', models.JSONField(blank=True, null=True)),
                ('saved_query', models.CharField(blank=True, max_length=200, null=True)),
                ('summary', models.CharField(default='Please write some summary for future reference', max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
