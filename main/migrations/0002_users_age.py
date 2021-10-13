# Generated by Django 3.2.8 on 2021-10-13 19:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='age',
            field=models.IntegerField(db_column='Age', null=True, validators=[django.core.validators.MaxValueValidator(120)], verbose_name='Age'),
        ),
    ]
