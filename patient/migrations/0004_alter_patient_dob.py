# Generated by Django 4.2.2 on 2025-01-29 20:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_alter_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='dob',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
