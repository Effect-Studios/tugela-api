# Generated by Django 4.2.2 on 2024-09-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_remove_jobsubmission_user_jobsubmission_freelancer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
