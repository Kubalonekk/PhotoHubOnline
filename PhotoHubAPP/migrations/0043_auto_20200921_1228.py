# Generated by Django 3.0.6 on 2020-09-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0042_post_ukryj_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
