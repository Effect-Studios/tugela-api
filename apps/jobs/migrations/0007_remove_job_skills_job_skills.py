# Generated by Django 4.2.2 on 2024-08-26 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_delete_profile'),
        ('jobs', '0006_jobbookmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='skills',
        ),
        migrations.AddField(
            model_name='job',
            name='skills',
            field=models.ManyToManyField(blank=True, to='users.skill'),
        ),
    ]