from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.views import View
from datetime import timedelta
import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required
from Long.models import ATM, Branch, Bank
from Hoang.models import Account, Customer, Transaction
from django.utils import timezone


# def IndexView(request):
#     return render(request, 'index.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


def signup_view(request):
    if request.method == "POST":
        data = request.POST.copy()
        full_name = data['fullname']
        id_type = data['id_type']
        id_no = data['id_no']
        gender = data['gender']
        bday = data['bday']
        phone_number = data['phone']
        email = data['emai']
        address = data['address']
        branch = data['branch_id']
        today = datetime.date.today()
        birth = datetime.datetime.strptime(bday, "%Y-%m-%d").date()
        age = (today - birth).days / 365
        ctg = Branch.objects.filter(branch_id=branch).first()
        try:
            if Customer.objects.filter(email=email).first():
                messages.error(request, 'Email đã tồn tại')
                return render(request, 'register.html')
            elif Customer.objects.filter(phone_number=phone_number).first():
                messages.error(request, 'Số điện thoại đã tồn tại')
                return render(request, 'register.html')
            elif Customer.objects.filter(id_no=id_no).first():
                messages.error(request, 'Khách hàng đã tồn tại')
                return render(request, 'register.html')
            elif age < 18:
                messages.error(request, 'Khách hàng chưa đủ tuổi để đăng kí')
                return render(request, 'register.html')
            else:
                Customer.objects.create(full_name=full_name,
                                        birthday=birth, gender=gender, address=address, phone_number=phone_number,
                                        email=email, id_type=id_type, id_no=id_no, branch_id=ctg)
                max_number = 9999999
                account_number = random.randint(0, max_number)
                get_customer = Customer.objects.filter(id_no=id_no).first()
                Account.objects.create(account_no=account_number, password='1', limit=100000000, balance=50000,
                                       create_day=datetime.date.today(),
                                       end_day=datetime.date.today() + timedelta(days=3650), status=1,
                                       customer_id=get_customer)
                return HttpResponse("Success")
        except:
            return HttpResponse('fail')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username1 = request.POST['usr']
        password1 = request.POST['pas']
        if Account.objects.filter(account_no=username1, password=password1).exists():
            request.session['usr'] = username1
            return render(request, 'dashboard.html')
        else:
            messages.error(request, "sai tên đăng nhập hoặc mật khẩu")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def withdrawal_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
        if request.method == 'POST':
            data = request.POST.copy()
            amount = request.POST['amount'] if 'amount' in request.POST else 0
            account = Account.objects.get(account_no=usr)
            amount = int(amount)
            atm = ATM.objects.get(atm_id=1)
            try:
                if amount % 10000 != 0:
                    messages.error(request, "Số tiền phải là bội số của 10000")
                    return render(request, 'withdrawal.html')
                elif amount == 0:
                    messages.error(request, "Số tiền không được bằng 0")
                    return render(request, 'withdrawal.html')
                elif account.balance - amount <= 49000:
                    messages.error(request, 'Tài khoản không đủ tiền')
                    return render(request, 'withdrawal.html')
                elif atm.atm_balance < amount or atm.atm_balance - amount < 0:
                    messages.error(request, 'Số tiền của cây ATM không đủ')
                    return render(request, 'withdrawal.html')
                elif amount > account.limit:
                    messages.error(request, "Số tiền không được lớn hơn hạn mức")
                    return render(request, "withdrawal.html")
                else:
                    account.balance = account.balance - amount - 1000
                    atm.atm_balance = atm.atm_balance - amount
                    Transaction.objects.create(transaction_type='RT',
                                               transaction_time=datetime.datetime.now(),
                                               balance=amount,
                                               transaction_fee=1000,
                                               status='1',
                                               atm_id_id='1',
                                               bank_id_id='CTG',
                                               card_no_id='123')
                    atm.save()
                    account.save()
                    return HttpResponse('Rút thành công %d VNĐ' % amount)
            except:
                return HttpResponse('Số tiền méo đúng rùi!')
        else:
            return render(request, 'withdrawal.html')
    return render(request, 'withdrawal.html')


# def another_view(request):
#     if request.method == "POST":
#         rut = withdrawal_view(request)
#         return render(request, 'another_value.html')
#     else:
#         return render(request, 'another_value.html')
