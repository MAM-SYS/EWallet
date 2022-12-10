from enum import Enum


class TransferType(Enum):
    Withdraw = 'Withdraw'
    Deposit = 'Deposit'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(field, field.value) for field in cls]


class TransferStatus(Enum):
    Init = 'Init'
    Pending = 'Pending'
    Succeed = 'Succeed'
    Failed = 'Failed'
    Canceled = 'Canceled'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(field, field.value) for field in cls]
