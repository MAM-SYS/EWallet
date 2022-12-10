from enum import StrEnum


class TransferType(StrEnum):
    Withdraw = 'Withdraw'
    Deposit = 'Deposit'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(field, field.value) for field in cls]


class TransferStatus(StrEnum):
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
