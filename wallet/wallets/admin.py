from django.contrib import admin
from wallets.models import Wallet, Transaction, Transfer

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Transfer)
