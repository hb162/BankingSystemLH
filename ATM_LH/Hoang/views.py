from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from datetime import timedelta
import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Long.models import ATM, Branch, Bank
from Hoang.models import Account, Customer, Transaction, Card
from django.db.models import Sum


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
                max_number = 9999999
                i = random.randint(0, max_number)
                i = str(i)
                Customer.objects.create(customer_id='KH' + i,
                                        full_name=full_name,
                                        birthday=birth,
                                        gender=gender,
                                        address=address,
                                        phone_number=phone_number,
                                        email=email,
                                        id_type=id_type,
                                        id_no=id_no,
                                        branch_id=branch)
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
            request.session.set_expiry(0)
            return redirect('dashboard')
        else:
            err = "Sai tên đăng nhập hoặc mật khẩu"
            return render(request, 'login.html', {"err": err})
    else:
        return render(request, 'login.html')


def forgot_view(request):
    if request.method == "POST":
        user = request.POST['usr']
        old_pass = request.POST['old-pas']
        pass1 = request.POST['pas1']
        pass2 = request.POST['pas2']
        if Account.objects.filter(account_no=user).exists():
            account = Account.objects.get(account_no=user)
            if account.password == old_pass:
                if pass1 == old_pass:
                    message = "Mật khẩu mới không được trùng mật khẩu cũ!"
                    return render(request, 'forgot_pass.html', {"message": message})
                elif pass1 != pass2:
                    message = "Mật khẩu nhập lại không khớp!"
                    return render(request, 'forgot_pass.html', {"message": message})
                else:
                    message = "Thành công!"
                    account.password = pass1
                    account.save()
                    return render(request, 'forgot_pass.html', {"message": message})
            else:
                message = "Mật khẩu cũ không đúng!"
                return render(request, 'forgot_pass.html', {"message": message})
        else:
            message = "Số tài khoản không tồn tại!"
            return render(request, 'forgot_pass.html', {'message': message})
    return render(request, 'forgot_pass.html')


def logout_view(request):
    try:
        del request.session['usr']
    except:
        pass
    return redirect('login')


def base_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
        account = Account.objects.get(account_no=usr)
        user = account.customer_id
        customer = Customer.objects.get(customer_id=user)
        name = customer.full_name
        context = {
            'usr': usr,
            'name': name,
        }
    return render(request, 'base.html', context)


def dashboard_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
    return render(request, 'dashboard.html', {'usr': usr})


def profile_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
        acc = Account.objects.get(account_no=usr)
        customer_id = acc.customer_id
        balance = acc.balance
        create_day = acc.create_day
        end_day = acc.end_day
        kh = acc.customer_id
        customer = Customer.objects.get(customer_id=customer_id).full_name
        context = {
            'usr': usr,
            'customer': customer,
            'balance': balance,
            'create_day': create_day,
            'end_day': end_day,
            'cus_id': kh,
        }
    return render(request, 'profile.html', context)


def withdrawal_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
        if request.method == 'POST':
            account = Account.objects.get(account_no=usr)
            atm = ATM.objects.get(atm_id='ATM01')
            atm_id = atm
            bank = Bank.objects.get(bank_id='CTG')
            bank_id = bank.bank_id
            card = Card.objects.filter(account_no=usr, card_type='2').first()
            dt = datetime.datetime.now()
            start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            end = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
            total = 0
            # tổng số tiền rút 1 ngày
            money = Transaction.objects.filter(card_no_id=card, transaction_type='RT').filter(transaction_time__gte=start, transaction_time__lte=end)
            for i in money:
                total = total + i.balance
            amount = request.POST['amount'] if 'amount' in request.POST else 0
            try:
                amount = int(amount)
            except:
                return HttpResponse("Lỗi amount")
            try:
                if total <= account.limit:
                    if amount % 10000 != 0:
                        err = "Số tiền phải là bội của 10000 VNĐ."
                        context = {
                            'message': err,
                            'usr': usr
                        }
                        return render(request, 'withdrawal.html', context)
                    elif amount == 0:
                        err = "Số tiền phải khác 0 VNĐ."
                        context = {
                            'message': err,
                            'usr': usr
                        }
                        return render(request, 'withdrawal.html', context)
                    elif total + amount >= account.limit:
                        err = "Số tiền vượt quá hạn mức."
                        context = {
                            'message': err,
                            'usr': usr
                        }
                        return render(request, "withdrawal.html", context)
                    elif account.balance - amount <= 49000:
                        err = "Tài khoản không đủ tiền để thực hiện giao dịch."
                        context = {
                            'message': err,
                            'usr': usr
                        }
                        return render(request, 'withdrawal.html', context)
                    elif atm.atm_balance < amount or atm.atm_balance - amount < 0:
                        err = "Cây ATM đã hết tiền."
                        context = {
                            'message': err,
                            'usr': usr
                        }
                        return render(request, 'withdrawal.html', context)
                    else:
                        account.balance = account.balance - amount - 1000
                        atm.atm_balance = atm.atm_balance - amount
                        Transaction.objects.create(transaction_type='RT',
                                                   transaction_time=datetime.datetime.now(),
                                                   balance=amount,
                                                   transaction_fee=1000,
                                                   content='Rut tien tai cay ATM',
                                                   receive_account=None,
                                                   status='1',
                                                   atm_id=atm_id,
                                                   bank_id=bank_id,
                                                   card_no_id=card,
                                                   receiver=None)
                        account.save()
                        atm.save()
                        return HttpResponse('Rút thành công %d VNĐ' % amount)
                else:
                    err = "Bạn đã tới hạn mức giao dịch!"
                    context = {
                        'usr': usr,
                        'message': err
                    }
                    return render(request, 'withdrawal.html', context)
            except:
                return HttpResponse('Số tiền méo đúng rùi!')
        else:
            return render(request, 'withdrawal.html', {'usr': usr})
    return render(request, 'withdrawal.html')


def another_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
        context = {
            'usr': usr
        }
        return render(request, 'another_value.html', context)


def open_card(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
    return render(request, 'open_card.html', {'usr': usr})


def transfer_internal(request):
    global context
    if request.session.has_key('usr'):
        usr = request.session['usr']
        account = Account.objects.get(account_no=usr)
        balance = account.balance
        context = {
            'usr': usr,
            'balance': balance,
        }
        if request.method == "POST":
            data = request.POST.copy()
            acc = data['sender']
            amount = data['amount']
            receive_account = data['receive-acc']
            content = data['content']
            try:
                amount = int(amount)
            except:
                return HttpResponse("Lỗi amount")
            try:
                receive_acc = Account.objects.filter(account_no=receive_account)
                if receive_acc.exists():
                    if amount == 0:
                        message = "Số tiền nhập phải khác 0."
                        context = {
                            'usr': usr,
                            'message': message
                        }
                        return render(request, 'transfer_internal.html', context)
                    elif amount > 100000000:
                        message = "Số tiền vượt quá hạn mức."
                        context = {
                            'usr': usr,
                            'message': message
                        }
                        return render(request, 'transfer_internal.html', context)
                    elif amount % 10000 != 0:
                        message = "Số tiền phải là bội số của 10000."
                        context = {
                            'usr': usr,
                            'message': message
                        }
                        return render(request, 'transfer_internal.html', context)
                    elif balance - amount <= 49000:
                        message = "Tài khoản không đủ tiền để thực hiện giao dịch."
                        context = {
                            'usr': usr,
                            'message': message
                        }
                        return render(request, 'transfer_external.html', context)
                    else:
                        request.session['sender'] = acc
                        request.session['balance'] = balance
                        request.session['receive-acc'] = receive_account
                        request.session['amount'] = amount
                        request.session['content'] = content
                        request.session.set_expiry(300)
                        return redirect('confirm_in')
                else:
                    message = "Số tài khoản không tồn tại."
                    context = {
                        'usr': usr,
                        'message': message
                    }
                    return render(request, 'transfer_internal.html', context)
            except:
                return HttpResponse("Lỗi")
    return render(request, 'transfer_internal.html', context)


def confirm_internal(request):
    global context
    if request.session.has_key('usr'):
        usr = request.session['usr']
        acc = request.session['sender']
        balance = request.session['balance']
        receive_account = request.session['receive-acc']
        amount = request.session['amount']
        content = request.session['content']
        context = {
            'usr': usr,
            'acc': acc,
            'balance': balance,
            'receive_acc': receive_account,
            'amount': amount,
            'content': content,
        }
        bank = Bank.objects.get(bank_id='CTG')
        bank_id = bank.bank_id
        atm = ATM.objects.get(atm_id='ATM01')
        card = Card.objects.filter(account_no=acc, card_type='2').first()
        sender = Account.objects.get(account_no=acc)
        receive_acc = Account.objects.get(account_no=receive_account)
        get_name = receive_acc.customer_id
        receiver = Customer.objects.get(customer_id=get_name).full_name
        if request.method == "POST":
            try:
                sender.balance = sender.balance - amount
                receive_acc.balance = receive_acc.balance + amount
                Transaction.objects.create(transaction_type='CKC',
                                           transaction_time=datetime.datetime.now(),
                                           balance=amount,
                                           transaction_fee=0,
                                           status='1',
                                           content=content,
                                           receive_account=receive_acc,
                                           atm_id=atm,
                                           bank_id=bank_id,
                                           card_no_id=card,
                                           receiver=receiver)
                sender.save()
                receive_acc.save()
                return HttpResponse("Thành công!")
            except:
                return HttpResponse("Lỗi")
    return render(request, 'confirm_transfer_in.html', context)


def transfer_external(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']
        user = Account.objects.get(account_no=usr)
        balance = user.balance
        context = {
            'usr': usr,
            'balance': balance,
        }
        if request.method == "POST":
            data = request.POST.copy()
            sender = data['sender']
            balance = data['balance']
            receive_acc = data['receive-acc']
            receiver = data['name']
            bank = data['ngan_hang'] if 'ngan_hang' in request.POST else 0
            branch = data['branch']
            content = data['content']
            amount = data['amount']
            try:
                amount = int(amount)
            except:
                return HttpResponse("Lỗi amount")
            try:
                if amount == 0:
                    message = "Số tiền nhập phải khác 0."
                    context = {
                        'usr': usr,
                        'message': message
                    }
                    return render(request, 'transfer_external.html', context)
                elif amount > 100000000:
                    message = "Số tiền vượt quá hạn mức."
                    context = {
                        'usr': usr,
                        'message': message
                    }
                    return render(request, 'transfer_external.html', context)
                elif amount % 10000 != 0:
                    message = "Số tiền phải là bội số của 10000."
                    context = {
                        'usr': usr,
                        'message': message
                    }
                    return render(request, 'transfer_external.html', context)
                elif balance - amount <= 49000:
                    message = "Tài khoản không đủ tiền để thực hiện giao dịch."
                    context = {
                        'usr': usr,
                        'message': message
                    }
                    return render(request, 'transfer_external.html', context)
                else:
                    request.session['sender'] = sender
                    request.session['balance'] = balance
                    request.session['receive-acc'] = receive_acc
                    request.session['name'] = receiver
                    request.session['ngan_hang'] = bank
                    request.session['branch'] = branch
                    request.session['content'] = content
                    request.session['amount'] = amount
                    request.session.set_expiry(300)
                    return redirect('confirm_ex')
            except:
                return HttpResponse("Lỗi ")
    return render(request, 'transfer_external.html', context)


def confirm_external(request):
    global context
    if request.session.has_key('usr'):
        usr = request.session['usr']
        sender = request.session['sender']
        balance = request.session['balance']
        receive_acc = request.session['receive-acc']
        receiver = request.session['name']
        bank = request.session['ngan_hang']
        branch = request.session['branch']
        get_branch = Branch.objects.get(branch_id=branch)
        branch_name = get_branch.branch_name
        content = request.session['content']
        amount = request.session['amount']
        context = {
            'sender': sender,
            'balance': balance,
            'receive_account': receive_acc,
            'receiver': receiver,
            'bank': bank,
            'branch': branch_name,
            'content': content,
            'amount': amount
        }
        account = Account.objects.get(account_no=sender)
        card = Card.objects.filter(account_no=sender, card_type='2').first()
        atm = ATM.objects.get(atm_id='ATM01')
        get_bank = Bank.objects.get(bank_id='CTG')
        bank_id = get_bank.bank_id
        if request.method == "POST":
            try:
                account.balance = account.balance - amount - 10000
                Transaction.objects.create(transaction_type='CKK',
                                           transaction_time=datetime.datetime.now(),
                                           balance=amount,
                                           transaction_fee=10000,
                                           receive_account=receive_acc,
                                           content=content,
                                           status=1,
                                           card_no_id=card,
                                           atm_id=atm,
                                           bank_id=bank_id,
                                           receiver=receiver)
                account.save()
                return HttpResponse("Thành công")
            except:
                return HttpResponse("Lỗi")
    return render(request, 'confirm_external.html', context)


def history_view(request):
    if request.session.has_key('usr'):
        usr = request.session['usr']

    return render(request, 'history_transaction.html')
