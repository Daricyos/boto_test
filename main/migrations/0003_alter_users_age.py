# Generated by Django 3.2.8 on 2021-10-13 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_users_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='age',
            field=models.IntegerField(db_column='Age', null=True, verbose_name='Age'),
        ),
    ]
