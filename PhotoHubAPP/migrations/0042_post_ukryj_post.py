# Generated by Django 3.0.6 on 2020-09-18 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0041_auto_20200917_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ukryj_post',
            field=models.ManyToManyField(blank=True, help_text='Użytkownicy ktorzy beda na tej liscie nie beda widzieli tego posta', related_name='ukryj_post_set', to='PhotoHubAPP.UserProfile'),
        ),
    ]
