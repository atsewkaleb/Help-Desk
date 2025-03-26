# Generated by Django 5.0.3 on 2024-08-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_is_approved_by_director_request_is_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('ict_director', 'ict_director'), ('team_leader', 'team_leader'), ('staff', 'staff'), ('client', 'client')], default='Client', max_length=100, verbose_name='Role'),
        ),
    ]
