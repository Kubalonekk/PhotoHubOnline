# Generated by Django 3.0.6 on 2020-05-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0018_auto_20200515_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='plec',
            field=models.CharField(blank=True, choices=[('', 'Podaj swoja plec'), ('Mężczyzna', 'Mężczyzna'), ('Kobieta', 'Kobieta')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(blank=True, choices=[('', 'Twój status'), ('W związku', 'W związku'), ('Wolny/a', 'Wolny/a'), ('To skomplikowane', 'To skomplikowane')], max_length=50, null=True),
        ),
    ]
