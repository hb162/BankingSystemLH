# Generated by Django 3.0.2 on 2020-02-11 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hoang', '0004_auto_20200210_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='receive_account',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
