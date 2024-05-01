# Generated by Django 5.0.3 on 2024-05-01 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_serie_movie_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielist',
            name='serie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.serie'),
        ),
        migrations.AlterField(
            model_name='movielist',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.movie'),
        ),
    ]