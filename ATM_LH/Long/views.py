from django.shortcuts import render, HttpResponse, Http404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, update_session_auth_hash
from django.db.models import Q
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Hoang.models import Account, Card, Customer
import random
import datetime
from datetime import timedelta
from django.contrib.auth.base_user import BaseUserManager
from django.contrib import messages
import string
# Create your views here.


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            current = User.objects.get(username=request.user)
            return render(request, 'password/password_change_success.html', {'name': current.username})
        else:
            return HttpResponse('Please check again')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password/password_change.html', {'form': form})

# mo them tai khoan ngan hang


def open_new_account(request):
    if request.method == 'POST':
        id_no = request.POST['id_no']
        try:
            if Customer.objects.filter(id_no=id_no):
                object_customer = Customer.objects.filter(id_no=id_no).first()
                max_account_no = 15
                limit = 100000000
                balance = 50000
                account_no = random.randint(10**(max_account_no-1), (10**max_account_no)-1)
                password = BaseUserManager().make_random_password()
                create_day = datetime.datetime.now()
                end_day = create_day + datetime.timedelta(days=10*365)
                status = 1
                Account.objects.create(
                    account_no=account_no,
                    password=password,
                    limit=limit,
                    balance=balance,
                    create_day=create_day,
                    end_day=end_day,
                    status=status,
                    customer_id=object_customer
                )
                messages.add_message(request, messages.SUCCESS, 'Mở thêm tài khoản thành công. Số tài khoản {}'
                                     .format(account_no))
                return redirect('open_account')
            else:
                messages.add_message(request, messages.WARNING, 'Số thẻ {} không có.'.format(id_no))
                return redirect('open_account')
        except:
            return Http404('Check again')
    else:
        return render(request, 'open/open_new_account.html', {})

# mo them the ngan hang


def open_new_card(request):
    if request.method == 'POST':
        id_account = request.POST['id_account']
        customer_name_input = request.POST['customer_name']
        try:
            if Account.objects.filter(account_no=id_account):
                account = Account.objects.filter(account_no=id_account).first()
                object_customer = Customer.objects.filter(customer_id=account.customer_id).first()
                if object_customer.full_name == customer_name_input:
                    max_card_number = 16
                    card_no = random.randint(10**(max_card_number - 1), (10**max_card_number) - 1)
                    create_date = datetime.datetime.today()
                    end_date = create_date + timedelta(3650)
                    card_type = request.POST['card_type']
                    status = 1
                    Card.objects.create(card_no=card_no,
                                        pin=BaseUserManager().make_random_password(6, string.digits),
                                        create_date=create_date, end_date=end_date,
                                        card_type=card_type,
                                        status=status,
                                        account_no=account)
                    messages.add_message(request, messages.SUCCESS, 'Mở thêm thẻ thành công. Số thẻ {}'.format(card_no))
                    return redirect('open_card')
                else:
                    messages.add_message(request, messages.ERROR, 'Kiểm tra lại tên tài khoản !')
                    return redirect('open_card')
            else:
                messages.error(request, 'Kiểm tra lại số tài khoản !')
                return redirect('open_card')
        except:
             return HttpResponse('Dont have this ID account {}'.format(id_account))
    else:
        return render(request, 'open/open_new_card.html', {})


def search_customer_anythings(request):
    if request.user.is_staff or request.user.is_superuser:
        object_customer = Customer.objects.all()
        query = request.GET.get('Q')
        if query:
            object_customer = object_customer.filter(
                Q(full_name__icontains=query) |
                Q(address__icontains=query) |
                Q(gender__icontains=query) |
                Q(email__contains=query) |
                Q(phone_number__exact=query))
            return render(request, 'customer/customer_result.html', {'query': query})
        else:
            return render(request, 'customer/customer_result.html', {'object_customer': object_customer})


def find_customer(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']

