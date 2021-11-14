# Generated by Django 3.2.7 on 2021-10-17 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0002_auto_20210911_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attending', models.BooleanField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.player')),
            ],
        ),
    ]
