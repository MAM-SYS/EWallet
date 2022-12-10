import uuid

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class Client(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)


class Bank(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    slug = models.CharField(max_length=50, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'banks'
        ordering = ['created_at']


class BankAccount(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    bank = models.ForeignKey(Bank, models.DO_NOTHING)
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)
    iban = models.CharField(max_length=34, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bank_accounts'
        ordering = ['created_at']
        unique_together = ['client', 'bank', 'iban']
