# Generated by Django 3.0.6 on 2020-08-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0026_auto_20200811_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='komentarze_counter',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, null=True),
        ),
    ]
