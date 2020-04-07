from rest_framework import serializers
from Hoang.models import Account, Customer, Card


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'url', 'full_name', 'birthday', 'gender', 'phone_number', 'email')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'url', 'account_no', 'password', 'balance', 'create_day', 'end_day', 'customer_id')


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'url', 'card_no', 'create_date', 'end_date', 'card_type', 'account_no')