# Generated by Django 3.0.6 on 2020-05-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0019_auto_20200515_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_counter',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='obserwowani',
            name='imie',
            field=models.CharField(help_text='Imię osoby która jest obserwowana', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='obserwowani',
            name='nazwisko',
            field=models.CharField(help_text='Nazwisko osoby która jest obserwowana', max_length=200, null=True),
        ),
    ]
