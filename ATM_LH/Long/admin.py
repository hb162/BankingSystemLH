from django.contrib import admin
from Hoang.models import *
from Long.models import *
# Register your models here.
# Hoang
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Card)



# Long
admin.site.register(Employee)
admin.site.register(HistoryMoney)
admin.site.register(Branch)
admin.site.register(ATM)
admin.site.register(Province)
admin.site.register(Bank)
