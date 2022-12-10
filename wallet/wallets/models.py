import uuid
from importlib import import_module

from banks.models import BankAccount, Client
from django.db import models
from django.db.models import Sum, Case, When, F
from django.db.models.functions import Coalesce
from dto_pack import TransferStatus, TransferTransitionTrigger
from dto_pack import TransferType
from khayyam import JalaliDatetime, teh_tz
from transitions import Machine, MachineError, State
from wallets.events import TransferStatusTransitions
from wallets.exceptions import TransferTransitionException

from utils import get_current_time
from utils import transition_callbacks


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    @property
    def balance(self):
        if balance := Transaction.objects.filter(wallet=self).aggregate(
                balance=Sum(
                    Coalesce(
                        Case(
                            When(transfer__type=TransferType.Deposit, then=F('amount')),
                            When(transfer__type=TransferType.Withdraw, then=-F('amount'))
                        ),
                        0),
                    output_field=models.DecimalField())
        )['balance']:
            return balance
        return 0

    def deposit(self, amount: int):
        # todo: deposit the amount into this wallet
        pass

    class Meta:
        db_table = 'wallets'
        ordering = ['created_at']


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['created_at']


def create_transfer_number():
    iran_datetime = JalaliDatetime(get_current_time().astimezone(teh_tz))
    return iran_datetime.strftime("%Y%m%d%H%M%S%f")


class Transfer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    number = models.CharField(max_length=25, unique=True, null=False, default=create_transfer_number)
    status = models.CharField(max_length=10, null=False, choices=TransferStatus.choices(), default=TransferStatus.Init)
    type = models.CharField(max_length=10, null=False, choices=TransferType.choices(), default=TransferType.Deposit)

    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    transaction = models.OneToOneField(Transaction, null=True, blank=True, on_delete=models.DO_NOTHING)

    from_bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, null=True, blank=True, related_name='withdraw_transfers')
    to_bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, null=True, blank=True, related_name='deposit_transfers')

    schedule_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def change_transfer_state(self, transition: TransferTransitionTrigger):
        if transfer := Transfer.objects.filter(number=self.number).first():
            transfer_state_machine = Machine(model='self',
                                             states=TransferStatus,
                                             initial=transfer.status,
                                             transitions=TransferStatusTransitions,
                                             queued=True)

            import_module('wallets.callbacks')
            for item in transition_callbacks:
                state: State = transfer_state_machine.get_state(item[1])
                state.add_callback(item[0], transition_callbacks[item])
            try:
                transfer_state_machine.dispatch(transition,
                                                self.number)
                transfer.status = transfer_state_machine.state.value
                transfer.save()
                return transfer
            except MachineError as e:
                raise TransferTransitionException(e.value)

    class Meta:
        db_table = 'transfers'
