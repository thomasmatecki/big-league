# Generated by Django 4.0.1 on 2022-01-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0004_alter_season_options_season_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='sport',
            field=models.CharField(choices=[('soccer', 'Soccer'), ('football', 'Flag Football'), ('kickball', 'Kickball')], default='football', max_length=30),
            preserve_default=False,
        ),
    ]
