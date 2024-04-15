# Generated by Django 5.0.4 on 2024-04-15 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SearchApp', '0008_alter_saveddata_options_alter_siteuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dividends',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='institutionalholders',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='majorholders',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='saveddata',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='siteuser',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='saveddata',
            name='username',
            field=models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SearchApp.siteuser'),
        ),
    ]
