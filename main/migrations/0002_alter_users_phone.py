# Generated by Django 3.2.8 on 2021-10-13 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.BigIntegerField(db_column='Phone', default=0, null=True),
        ),
    ]
