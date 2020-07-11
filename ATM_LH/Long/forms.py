from django.forms import Form, ModelForm, DateTimeField, DateField, widgets
from django import forms
from Hoang.models import Customer, Account, Card
from Long.models import Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, ButtonHolder
Sex = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('No', 'Unknown'),
    )
Type = (
    ('CMND', 'Chứng minh nhân dân'),
    ('TCC', 'Thẻ căn cước'),
    ('HC', 'Hộ chiếu'),
)
Type_card = (
        ('1', 'Thẻ tín dụng'),
        ('2', 'Thẻ ATM'),
        ('3', 'Thẻ ghi nợ'),
        ('4', 'Thẻ đảm bảo'),
        ('5', 'Thẻ Visa'),
    )


class OpenNewAccount(forms.Form):
    id_type = forms.ChoiceField(choices=Type)
    id_no = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Nhập số thẻ '}
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False


class OpenNewCard(forms.Form):
    account_no = forms.CharField(required=True, max_length=15)
    full_name = forms.CharField(max_length=32)
    card_type = forms.ChoiceField(choices=Type_card, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False


class UpdateProfile(ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ['full_name', 'birthday', 'phone_number', 'gender', 'address', 'email', 'branch']

    def __init__(self, *args, **kwargs):
        super(UpdateProfile, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'full_name',
            'birthday',
            'phone_number',
            'gender',
            'address',
            'email',
            'branch',
            Submit('submit', 'Lưu thay đổi', css_class='btn btn-success')
        )
        self.helper.form_show_labels = False


class ProfileCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'birthday', 'phone_number', 'gender', 'address', 'email',
                  'id_type', 'id_no', 'branch']

    def __init__(self, *args, **kwargs):
        super(ProfileCustomer, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['full_name'].widget.attrs['disabled'] = 'disabled'
            self.fields['birthday'].widget.attrs['disabled'] = 'disabled'
            self.fields['phone_number'].widget.attrs['disabled'] = 'disabled'
            self.fields['gender'].widget.attrs['disabled'] = 'disabled'
            self.fields['address'].widget.attrs['disabled'] = 'disabled'
            self.fields['email'].widget.attrs['disabled'] = 'disabled'
            self.fields['id_type'].widget.attrs['disabled'] = 'disabled'
            self.fields['id_no'].widget.attrs['disabled'] = 'disabled'
            self.fields['branch'].widget.attrs['disabled'] = 'disabled'


class SearchCustomer(forms.Form):
    full_name = forms.CharField(max_length=32, required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Nhập tên khách hàng'
        }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={
            'placeholder': 'Nhập email khách hàng '
        }))
    branch = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Nhập chi nhánh '
        }))
    bank = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Nhập ngân hàng  '}
    ))
    phone_number = forms.CharField(required=False, max_length=12, widget=forms.NumberInput(
        attrs={
            'placeholder': 'Nhập số điện thoại '
        }))

    def __init__(self, *args, **kwargs):
        super(SearchCustomer, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False


class EmployeeFind(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name']