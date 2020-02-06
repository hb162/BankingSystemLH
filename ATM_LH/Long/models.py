from django.db import models
from django.db.models import Q


class Province(models.Model):
    province_id = models.CharField(max_length=2, unique=True)
    province_name = models.TextField()

    def __str__(self):
        return self.province_id


class Bank(models.Model):
    bank_id = models.CharField(max_length=8, unique=True)
    bank_name = models.TextField()
    bank_headquarters = models.TextField()
    bank_phone_number = models.CharField(max_length=10)
    branches = models.ManyToManyField(Province, through="Branch")

    def __str__(self):
        return self.bank_name, self.bank_id


class Branch(models.Model):
    province = models.ForeignKey(Province, to_field='province_id', on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, to_field='bank_id', on_delete=models.CASCADE)
    branch_id = models.CharField(max_length=5, primary_key=True)
    branch_name = models.CharField(max_length=100)
    branch_address = models.TextField()

    def __str__(self):
        return self.branch_id, self.branch_name


class Employee(models.Model):
    branch = models.ForeignKey(Branch, to_field='branch_id', on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=5, unique=True)
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=32)
    emp_password = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name, self.branch_id


class ATM(models.Model):
    choice = (
        ('1', 'Active'),
        ('0', 'Deactive'),
    )
    employee = models.OneToOneField(Employee, to_field='employee_id', on_delete=models.CASCADE)
    atm_id = models.CharField(max_length=5, unique=True)
    address = models.TextField()
    atm_balance = models.BigIntegerField()
    status = models.CharField(max_length=1, choices=choice)

    def __str__(self):
        return self.atm_id


class HistoryMoney(models.Model):
    history_id = models.CharField(max_length=3, unique=True)
    atm = models.ForeignKey(ATM, to_field='atm_id', on_delete=models.CASCADE)
    history_time = models.DateTimeField()
    money = models.BigIntegerField()

    def __str__(self):
        return self.history_id
