# Generated by Django 4.2.7

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_alter_metric_average_age_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metric',
            name='average_experience',
        ),
    ]
