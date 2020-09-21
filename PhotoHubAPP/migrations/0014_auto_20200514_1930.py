# Generated by Django 3.0.6 on 2020-05-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0013_remove_userprofile_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='opis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(blank=True, choices=[('', 'Twój status'), ('A', 'W związku'), ('B', 'Wolny/a'), ('C', 'To skomplikowane')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wyksztalcenie',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]