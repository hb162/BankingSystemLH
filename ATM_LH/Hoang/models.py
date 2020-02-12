from django.db import models
from Long.models import Branch, ATM, Bank


class Customer(models.Model):
    Sex = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('No', 'Unknown'),
    )
    type = (
        ('CMND', 'Chứng minh nhân dân'),
        ('TCC', 'Thẻ căn cước'),
        ('HC', 'Hộ chiếu'),
    )
    customer_id = models.CharField(max_length=10, unique=True)
    branch = models.ForeignKey(Branch, to_field='branch_id', on_delete=models.CASCADE)
    id_type = models.CharField(max_length=4, choices=type)
    id_no = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=32)
    birthday = models.DateField()
    gender = models.CharField(max_length=2, choices=Sex)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.customer_id


class Account(models.Model):
    choice = (
        ('1', 'Active'),
        ('2', 'Dormant'),
        ('0', 'Inactive'),
    )
    customer = models.ForeignKey(Customer, to_field='customer_id', on_delete=models.CASCADE)
    account_no = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    limit = models.BigIntegerField()
    balance = models.BigIntegerField()
    create_day = models.DateField()
    end_day = models.DateField()
    status = models.CharField(max_length=1, choices=choice)

    def __str__(self):
        return self.account_no


class Card(models.Model):
    type = (
        ('1', 'Thẻ tín dụng'),
        ('2', 'Thẻ ATM'),
        ('3', 'Thẻ ghi nợ'),
        ('4', 'Thẻ đảm bảo'),
        ('5', 'Thẻ Visa'),
    )
    choice = (
        ('1', 'Active'),
        ('0', 'Deactive'),
    )
    account_no = models.ForeignKey(Account, to_field='account_no', on_delete=models.CASCADE)
    card_no = models.CharField(max_length=16, unique=True)
    pin = models.CharField(max_length=6)
    create_date = models.DateField()
    end_date = models.DateField()
    card_type = models.CharField(max_length=1, choices=type)
    status = models.CharField(max_length=1, choices=choice)

    def __str__(self):
        return self.card_no


class Transaction(models.Model):
    type = (
        ('RT', 'withdrawal'),
        ('CKC', 'internal transfer'),
        ('CKK', 'interbank transfer'),
    )
    choice = (
        ('1', 'success'),
        ('0', 'fail'),
    )
    transaction_type = models.CharField(max_length=3, choices=type)
    transaction_time = models.DateTimeField()
    balance = models.BigIntegerField(default=0)
    card_no = models.ForeignKey(Card, to_field='card_no', on_delete=models.CASCADE)
    transaction_fee = models.IntegerField()
    receiver = models.CharField(max_length=50, null=True, blank=True)
    receive_account = models.CharField(max_length=12, null=True, blank=True)
    content = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=1, choices=choice)
    atm = models.ForeignKey(ATM, to_field='atm_id', on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, to_field='bank_id', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, to_field='branch_id', default='CTG01', on_delete=models.CASCADE)
