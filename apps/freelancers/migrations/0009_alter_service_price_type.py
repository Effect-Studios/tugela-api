# Generated by Django 4.2.2 on 2024-09-06 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0008_freelancer_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='price_type',
            field=models.CharField(choices=[('per_project', 'Per Project'), ('per_hour', 'Per Hour'), ('per_week', 'Per Week'), ('per_month', 'Per Month'), ('per_year', 'Per Year')], max_length=50),
        ),
    ]
