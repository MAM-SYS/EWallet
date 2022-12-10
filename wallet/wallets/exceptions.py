from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ClientNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Client not found exception')
    default_code = 'not_found'


class WalletConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Wallet already exists for this client')
    default_code = 'conflict'


class TransferNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Client not found exception')
    default_code = 'not_found'


class TransferTransitionException(APIException):
    def __init__(self, message):
        self.status_code = 400
        self.detail = _(f'{message}')
        self.code = 'error'
