# Generated by Django 3.1.2 on 2020-11-17 22:42

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
            name='Note',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('topic', models.CharField(max_length=30)),
                ('text', models.TextField(blank=True, max_length=4092, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_edit', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
