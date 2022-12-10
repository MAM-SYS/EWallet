from django.contrib import admin
from banks.models import Bank, BankAccount, Client

admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Client)