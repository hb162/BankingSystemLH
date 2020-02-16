from django.shortcuts import render, HttpResponse, Http404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, update_session_auth_hash
from django.db.models import Q
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Hoang.models import Account, Card, Customer, Transaction
from Long.models import Employee
import random
import datetime
from datetime import timedelta
from django.contrib.auth.base_user import BaseUserManager
from django.contrib import messages
from django.db import models
from django.core.paginator import Paginator
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
        id_type = request.POST['id_type']
        try:
            if Customer.objects.filter(id_no=id_no, id_type=id_type):
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
        if request.method == "GET":
            query = request.GET.get('Q')
            if query:
                object_customer = object_customer.filter(
                    Q(full_name__contains=query) |
                    Q(address__contains=query) |
                    Q(gender__contains=query) |
                    Q(email__contains=query) |
                    Q(phone_number__exact=query)).distinct()
                return render(request, 'customer/customer_result.html', {'object_customer': object_customer})
            # else:
            #     messages.add_message(request, messages.WARNING, "Không tìm thấy kết quả mong muốn")
            #     return redirect('search_customer')
            else:
                return render(request, 'customer/customer_result.html', {'object_customer': object_customer})
        elif request.method == "POST":
            email = request.POST['email']
            full_name = request.POST['full_name']
            phone_number = request.POST['phone_number']
            # gender = request.POST['gender']
            branch = request.POST['branch']
            bank = request.POST['bank']
            if object_customer:
                if email:
                    object_customer = object_customer.filter(email__icontains=email)
                elif phone_number:
                    object_customer = object_customer.filter(phone_number__exact=phone_number)
                elif full_name is not None and bank is not None:
                    object_customer = object_customer.filter(full_name__icontains=full_name,
                                                             branch__bank_id__bank_name__icontains=bank)
                elif full_name is not None and bank is not None and branch is not None:
                    object_customer = object_customer.filter(full_name__icontains=full_name,
                                                             branch__bank__bank_name__icontains=bank,
                                                             branch__bank_id__bank_name__icontains=bank)
                else:
                    return HttpResponse("ko tim dc")
                paginator = Paginator(object_customer, 3)
                page = request.GET.get('page')
                posts = paginator.get_page(page)
                return render(request, 'customer/customer_result.html', {'posts': posts,
                                                                         'object_customer': object_customer})
            else:
                return render(request, 'customer/customer_result.html', {'object_customer': object_customer})


def detail_customer_profile(request, customer_id):
    if request.method == "GET":
        object_customer = Customer.objects.get(customer_id=customer_id)
        full_name = object_customer.full_name
        gender = object_customer.gender
        address = object_customer.address
        birthday = object_customer.birthday
        phone_number = object_customer.phone_number
        email = object_customer.email
        branch_name = object_customer.branch.branch_name
        bank_name = object_customer.branch.bank_id.bank_name
        id_type = object_customer.id_type
        id_no = object_customer.id_no
        context = {
            'full_name': full_name,
            'gender': gender,
            'address': address,
            'birthday': birthday,
            'phone_number': phone_number,
            'email': email,
            'branch_name': branch_name,
            'bank_name': bank_name,
            'id_type': id_type,
            'id_no': id_no,
        }
        return render(request, 'customer/customer_profile.html', context)
    else:
        return render(request, 'customer/customer_profile.html')


def show_profile_account(request):
    object_account = Account.objects.all()
    if request.method == "POST":
        account_no = request.POST['account_no']
        # result_account.customer_id
        if object_account.filter(account_no=account_no).exists():
            result_account = object_account.get(account_no=account_no)
            result_customer = Customer.objects.get(customer_id=result_account.customer_id)
            result_card = Card.objects.filter(account_no_id=account_no)
            result_transaction = Transaction.objects.filter(card_no=result_card)
            context_object = {
                'result_account': result_account,
                'result_customer': result_customer,
                'result_card_objects': result_card,
                'result_transactions': result_transaction,
            }
            return render(request, 'account/show_account.html', context_object)
        else:
            messages.add_message(request, messages.ERROR, 'Số tài khoản vừa nhập không tồn tại')
            return render(request, 'account/show_account.html', {'message': messages})
    else:
        return render(request, 'account/show_account.html', {'object_account': object_account})


def show_profile_atm(request):
    pass
