# Generated by Django 3.0.2 on 2020-03-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Long', '0002_auto_20200310_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='emp_job',
            field=models.CharField(default='A', max_length=50),
        ),
        migrations.AlterField(
            model_name='historymoney',
            name='money',
            field=models.BigIntegerField(),
        ),
    ]