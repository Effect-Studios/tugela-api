# Generated by Django 4.2.2 on 2024-08-16 12:01

import apps.extras.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(max_length=10)),
                ('iso', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('factor', models.CharField(max_length=64, validators=[apps.extras.models.validate_integer])),
                ('name', models.CharField(max_length=64)),
                ('precision', models.PositiveSmallIntegerField(default=0)),
                ('symbol', models.CharField(blank=True, max_length=2, null=True)),
                ('_type', models.CharField(choices=[('fiat', 'Fiat'), ('crypto', 'Crypto')], default='fiat', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
