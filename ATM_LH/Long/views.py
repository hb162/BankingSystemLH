from django.shortcuts import render, HttpResponse, Http404, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.urls import reverse
from .serializers import AccountSerializer
from django.views.generic import ListView, DetailView, View, TemplateView, FormView, UpdateView
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import BaseUserManager
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.views import APIView
from .serializers import CustomerSerializer
from rest_framework.response import Response
from Hoang.models import Account, Card, Customer, Transaction
from Long.models import Employee, ATM, HistoryMoney, Bank, Branch
from random import randint
import datetime
from datetime import timedelta
import string
from .forms import UpdateProfile, OpenNewCard, OpenNewAccount, ProfileCustomer, SearchCustomer, EmployeeFind


# Create your views here.


# @decorators.login_required(login_url='/Long/login/')
class HomePage(TemplateView):
    template_name = 'home.html'


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            current = User.objects.get(username=request.user)
            auth.logout(request)
            return render(request, 'password/password_change_success.html', {'name': current.username})
        else:
            return HttpResponse('Please check again')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password/password_change.html', {'form': form})


class OpenAccountView(View):

    @staticmethod
    def get(request):
        form = OpenNewAccount()
        context = {
            'f': form
        }
        return render(request, 'open/form_new_account.html', context)

    @staticmethod
    def post(request):
        form = OpenNewAccount(data=request.POST)
        if form.is_valid():
            id_no = form.cleaned_data['id_no']
            id_type = form.cleaned_data['id_type']
            try:
                object_customer = Customer.objects.get(id_no=id_no, id_type=id_type)
                create_day = datetime.datetime.now()
                account_no = random_number(15)
                Account.objects.create(account_no=account_no,
                                       password=BaseUserManager().make_random_password(),
                                       limit=100000000,
                                       balance=50000,
                                       create_day=create_day,
                                       end_day=create_day + datetime.timedelta(days=10 * 365),
                                       status=1,
                                       customer_id=object_customer
                                       )
                messages.add_message(request, messages.SUCCESS, 'Mở thêm tài khoản thành công. Số tài khoản {}'
                                     .format(object_customer.account_set.last()))
                return redirect('open_account_form')
            except Customer.DoesNotExist:
                messages.add_message(request, messages.WARNING, 'Vui lònng kiểm tra lại.')
                return redirect('open_account_form')


class OpenCardView(View):
    template_name = 'open/form_new_card.html'

    def get(self, request):
        form = OpenNewCard()
        context = {
            'f': form
        }
        return render(request, self.template_name, context)

    @staticmethod
    def post(request):
        form = OpenNewCard(data=request.POST)
        if form.is_valid():
            try:
                account = Account.objects.get(account_no=form.cleaned_data['account_no'])
                if form.cleaned_data['full_name'] == account.customer.full_name:
                    create_time = datetime.datetime.today()
                    card_no = random_number(16)
                    Card.objects.create(card_no=card_no,
                                        pin=BaseUserManager().make_random_password(6, string.digits),
                                        create_date=create_time,
                                        end_date=create_time + timedelta(365 * 10),
                                        card_type=form.cleaned_data['card_type'],
                                        status=1,
                                        account_no=account
                                        )
                    messages.add_message(request, messages.SUCCESS, 'Mở thêm thẻ thành công. Số thẻ {}'.format(card_no))
                    return redirect('open_card_form')
                else:
                    messages.add_message(request, messages.WARNING, 'Kiểm tra lại tên tài khoản !')
                    return redirect('open_card_form')
            except Account.DoesNotExist:
                messages.add_message(request, messages.ERROR,
                                     'Không có tài khoản {}'.format(form.cleaned_data['account_no']))
                return redirect('open_card_form')


class SearchCustomerView(ListView):
    paginate_by = 2
    template_name = 'customer/customer_result.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchCustomerView, self).get_context_data()
        context['f'] = SearchCustomer()
        context['object_customer'] = Customer.objects.all()[0:8]
        return context

    def get_queryset(self):
        query = self.request.GET.get('Q')
        object_customer = Customer.objects.all()
        if query:
            object_customer = Customer.objects.filter(
                Q(full_name__icontains=query) |
                Q(address__icontains=query) |
                Q(gender__icontains=query) |
                Q(email__icontains=query) |
                Q(phone_number__exact=query)).distinct()
        paginator = Paginator(object_customer, object_customer.count())
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj

    def post(self, request):
        form = SearchCustomer(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            branch = form.cleaned_data['branch']
            bank = form.cleaned_data['bank']
            kwargs = {}
            if email:
                kwargs['email__icontains'] = email
            if phone_number:
                kwargs['phone_number__exact'] = phone_number
            if full_name is not None and bank is not None:
                kwargs['full_name__icontains'] = full_name
                kwargs['branch__bank_id__bank_name__icontains'] = bank
            if branch is not None:
                kwargs['branch__branch_name__icontains'] = branch
            object_customer = Customer.objects.filter(**kwargs)
            paginator = Paginator(object_customer, 2)
            page_obj = paginator.get_page(self.request.GET.get('page'))
            context = {
                       'object_customer': object_customer,
                       'page_obj': page_obj,
                       'f': form
                       }
            return render(request, self.template_name, context)
        return redirect('search_customer')


class DetailCustomerView(DetailView):
    model = Customer
    template_name = 'customer/customer_profile.html'
    context_object_name = 'object_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['f'] = ProfileCustomer(instance=self.object)
        return context


@login_required
def update_profile_customer(request, id_cus):
    object_customer = get_object_or_404(Customer, pk=id_cus)
    form = UpdateProfile(data=request.POST or None, instance=object_customer)
    if request.method == 'POST':
        if form.is_valid():
            object_customer = form.save(commit=False)
            object_customer.save()
            return redirect('detail_customer_view', id_cus)
    return render(request, 'customer/update_profile_customer.html', {'f': form, 'object': object_customer})


@login_required
def show_profile_account(request):
    object_account = Account.objects.all()
    if request.method == "POST":
        account_no = request.POST['account_no']
        if object_account.filter(account_no=account_no).exists():
            result_account = object_account.get(account_no=account_no)
            result_customer = Customer.objects.get(customer_id=result_account.customer_id)
            result_card = Card.objects.filter(account_no_id=account_no)
            result_transaction = Transaction.objects.filter(card_no__account_no=account_no) \
                .order_by('-transaction_time')
            money = 0
            for a in result_transaction:
                if a.status == '1':
                    money += a.balance
            context = {
                'result_account': result_account,
                'result_customer': result_customer,
                'result_card_objects': result_card,
                'result_transactions': result_transaction,
                'money': f"{money:,}",
            }
            return render(request, 'account/show_account.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Số tài khoản vừa nhập không tồn tại')
            return render(request, 'account/show_account.html', {'message': messages})
    else:
        return render(request, 'account/show_account.html', {'object_account': object_account})


@login_required
def search_atm(request):
    if request.user.is_staff or request.user.is_superuser:
        atm_object = ATM.objects.all()
        bank_object = Bank.objects.all()
        branch_object = Branch.objects.all()
        context = {
            'atm_object': atm_object,
            'bank_object': bank_object,
            'branch_object': branch_object,
        }
        if request.method == 'POST':
            branch = request.POST['branch']
            atm_no = request.POST['atm_no']
            bank_name = Branch.objects.get(branch_name=branch)
            try:
                atm_object = atm_object.get(atm_id=atm_no, employee__branch__bank_id=bank_name.bank_id,
                                            employee__branch__branch_name=branch)
                return redirect('atm_profile', atm_id=atm_object.atm_id)
            except ATM.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Không tìm thấy ATM mã số {}".format(atm_no))
                return render(request, 'atm/atm_search.html', context)
        else:
            return render(request, 'atm/atm_search.html', context)
    else:
        return Http404("You are not login")


@login_required
def atm_profile(request, atm_id):
    atm = ATM.objects.get(atm_id=atm_id)
    employee = Employee.objects.get(employee_id=atm.employee_id)
    trans = Transaction.objects.filter(atm_id=atm_id).order_by('-transaction_time')
    history_money = HistoryMoney.objects.filter(atm_id=atm_id).order_by('-history_time')[:4]
    money_result = 0
    count_success = 0
    count_error = 0
    for a in trans:
        if a.status == '1':
            count_success += 1
            money_result += a.balance
        elif a.status == '0':
            count_error += 1
    context1 = {
        'atm': atm,
        'employee': employee,
        'trans': trans,
        'money_result': money_result,
        'history_money': history_money,
        'count_success': count_success,
        'count_error': count_error,
    }
    if request.method == 'POST':
        time_start = request.POST['time_start']
        time_end = request.POST['time_end']
        try:
            trans = trans.filter(transaction_time__gte=time_start, transaction_time__lte=time_end)
            money_result = 0
            count_success = 0
            count_error = 0
            for a in trans:
                if a.status == '1':
                    count_success += 1
                    money_result += a.balance
                elif a.status == '0':
                    count_error += 1
            context = {
                'atm': atm,
                'employee': employee,
                'trans': trans,
                'money_result': money_result,
                'history_money': history_money,
                'count_success': count_success,
                'count_error': count_error,
            }
            messages.add_message(request, messages.ERROR, 'Không tim thấy yêu cầu ')
            return render(request, 'atm/atm_profile.html', context)
        except Transaction.DoesNotExist:
            return Http404('Error')
    return render(request, 'atm/atm_profile.html', context1)


@login_required
def show_trans_account(request, trans_id):
    trans_current = Transaction.objects.get(id=trans_id)
    trans_object = Transaction.objects.filter(card_no=trans_current.card_no)
    context = {
        'trans_current': trans_current,
        'trans_object': trans_object,
    }
    return render(request, 'trans/trans_detail.html', context)


@login_required
def lock_account(request, account_no):
    account = Account.objects.filter(account_no=account_no)
    account.update(status='0')
    return render(request, 'account/open_close.html')


@login_required
def open_acc(request, account_no):
    account = Account.objects.filter(account_no=account_no)
    account.update(status='1')
    return render(request, 'account/open_close.html')


@login_required
def show_history_money_detail(request, atm_id):
    history_atm_money = HistoryMoney.objects.filter(atm_id=atm_id)
    context = {
        'htr_money': history_atm_money,
        'atm_id': atm_id
    }
    if request.method == 'POST':
        money = request.POST['money']
        if int(money) > 500000000 or int(money) < 1000000:
            messages.add_message(request, messages.ERROR, 'Số tiền phải trong khoảng 1000,000 VND đến 500,000,000 VND ')
        else:
            HistoryMoney.objects.create(history_id=random_number(3), history_time=datetime.datetime.now(),
                                        money=int(money), atm_id=atm_id)
            messages.add_message(request, messages.SUCCESS, 'Them thanh cong')
    return render(request, 'atm/atm_add_money.html', context)


@login_required
def update_profile_atm(request, atm_id, branch_id):
    atm = ATM.objects.filter(atm_id=atm_id)
    atm_current = ATM.objects.get(atm_id=atm_id)
    employee_objects = Employee.objects.filter(branch_id=branch_id)
    # employ_id = set(ATM.objects.filter(employee__branch__bank_id=branch_id).values_list('employee_id'))
    if request.method == 'POST':
        address = request.POST['address']
        employee_input = request.POST['employee']
        try:
            atm.update(address=address, employee=employee_input)
            return HttpResponse('Thanh cong')
        except ATM.DoesNotExist:
            messages.add_message(request, messages.WARNING, 'Nhan vien da quan ly ATM')
    return render(request, 'atm/atm_update.html', {'employee_object': employee_objects,
                                                   'atm_id': atm_id,
                                                   'branch_id': branch_id,
                                                   'atm': atm_current})


@login_required
def trans_detail(request, trans_id):
    trans_obj = Transaction.objects.get(trans_id=trans_id)
    card = Card.objects.get(card_no=trans_obj.card_no)
    context = {
        'trans_obj': trans_obj,
        'card': card,
    }
    return render(request, 'trans/trans_detail.html', context)


def random_number(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


class CustomerRudView(APIView):

    @staticmethod
    def get(request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


def AccountReview(request, customer_id):
    try:
        account = Account.objects.filter(customer_id=customer_id)
    except Account.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = AccountSerializer(account, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=405)


class EmployeeView(View):
    template_name = 'classbaseview/employee_view.html'

    def get(self, request, employee_id):
        employee_object = Employee.objects.get(employee_id=employee_id)
        form = EmployeeFind(instance=employee_object)
        context = {
            'employee': employee_object,
            'f': form
        }
        return render(request, self.template_name, context)

    def post(self, request, employee_id):
        employee_object = Employee.objects.get(employee_id=employee_id)
        form = EmployeeFind(data=request.POST, instance=employee_object)
        if form.is_valid():
            employee_object = form.save()
            employee_object.save()
            messages.add_message(request, messages.SUCCESS, 'Success change name')
            return redirect('employee', employee_id=employee_id)
        return Http404('Error')


class EmployeeListView(ListView):
    model = Employee
    template_name = 'classbaseview/employee_list_view.html'
    paginate_by = 2
    context_object_name = 'queryset'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_object = Employee.objects.all()
        context['employee_object'] = employee_object
        context['page'] = 'page'
        print(reverse('employee_listview'))
        return context


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'classbaseview/employee_detail_view.html'


class EmployeeTemplateView(TemplateView):
    template_name = 'classbaseview/employee_template_view.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Hello'
        return context
