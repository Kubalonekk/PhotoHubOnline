# Generated by Django 3.0.6 on 2020-08-13 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoHubAPP', '0029_auto_20200812_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObserwowaniPowiadomienia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obserwacja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhotoHubAPP.Obserwowani')),
            ],
        ),
    ]