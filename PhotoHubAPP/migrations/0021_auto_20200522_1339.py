# Generated by Django 3.0.6 on 2020-05-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0020_auto_20200518_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='plec',
            field=models.CharField(blank=True, choices=[('', 'Podaj swoja plec'), ('Mezczyzna', 'Męzczyzna'), ('Kobieta', 'Kobieta')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(blank=True, choices=[('', 'Twój status'), ('W zwiazku', 'W zwiazku'), ('Wolny/a', 'Wolny/a'), ('To skomplikowane', 'To skomplikowane')], max_length=50, null=True),
        ),
    ]
