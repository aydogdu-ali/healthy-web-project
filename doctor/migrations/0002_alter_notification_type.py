# Generated by Django 4.2.2 on 2025-01-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('New Appointment', 'New Appointment'), ('Appointmen Cancelled', 'Appointmen Cancelled')], max_length=100),
        ),
    ]
