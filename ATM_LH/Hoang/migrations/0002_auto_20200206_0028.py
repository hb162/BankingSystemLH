# Generated by Django 3.0.2 on 2020-02-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hoang', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='end_day',
            field=models.DateField(),
        ),
    ]