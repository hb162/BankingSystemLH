# Generated by Django 3.0.2 on 2020-01-15 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Long', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('limit', models.BigIntegerField()),
                ('balance', models.BigIntegerField()),
                ('create_day', models.DateField()),
                ('end_day', models.DateTimeField()),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Dormant'), ('0', 'Inactive')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_no', models.CharField(max_length=16, unique=True)),
                ('pin', models.CharField(max_length=6)),
                ('create_date', models.DateField()),
                ('end_date', models.DateField()),
                ('card_type', models.CharField(choices=[('1', 'Thẻ tín dụng'), ('2', 'Thẻ ATM'), ('3', 'Thẻ ghi nợ'), ('4', 'Thẻ đảm bảo'), ('5', 'Thẻ Visa')], max_length=1)),
                ('status', models.CharField(choices=[('1', 'Active'), ('0', 'Deactive')], max_length=1)),
                ('account_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hoang.Account', to_field='account_no')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('RT', 'withdrawal'), ('CKC', 'internal transfer'), ('CKK', 'interbank transfer')], max_length=3)),
                ('transaction_time', models.DateTimeField()),
                ('balance', models.BigIntegerField()),
                ('transaction_fee', models.IntegerField()),
                ('status', models.CharField(choices=[('1', 'success'), ('0', 'fail')], max_length=1)),
                ('atm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Long.ATM', to_field='atm_id')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Long.Bank', to_field='bank_id')),
                ('card_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hoang.Card', to_field='card_no')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=10, unique=True)),
                ('id_type', models.CharField(choices=[('CMND', 'Chứng minh nhân dân'), ('TCC', 'Thẻ căn cước'), ('HC', 'Hộ chiếu')], max_length=4)),
                ('id_no', models.CharField(max_length=15, unique=True)),
                ('full_name', models.CharField(max_length=32)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Man'), ('W', 'Woman'), ('No', 'Unknown')], max_length=2)),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Long.Branch', to_field='branch_id')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hoang.Customer', to_field='customer_id'),
        ),
    ]
