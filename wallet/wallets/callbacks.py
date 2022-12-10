import json
from typing import Dict

from dto_pack import TransferStatus, TransferTransitionTrigger
from dto_pack.enum import TransferType
from wallet.nng import pub
from wallets.exceptions import TransferNotFoundException
from wallets.models import Transfer

from utils import register_transition_callback


@register_transition_callback(exit_trigger=TransferStatus.Init)
def submit_transfer_request(transfer_number: str):
    if not (transfer := Transfer.objects.filter(number=transfer_number).first()):
        raise TransferNotFoundException()

    if transfer.type == TransferType.Withdraw:
        if transfer.to_bank_account and transfer.scheduled_at:
            data: Dict = {"transition": TransferTransitionTrigger.Submit,
                          "client_id": str(transfer.client_id).replace('-', ''),
                          "amount": float(transfer.amount),
                          "transfer_number": transfer.number,
                          "type": TransferType.Deposit.value,
                          "scheduled_at": transfer.scheduled_at.isoformat()}

            pub.send(f'transfer:{json.dumps(data)}'.encode('utf-8'))


@register_transition_callback(enter_trigger=TransferStatus.Canceled)
def cancel_transfer_request(transfer_number: str):
    if not (transfer := Transfer.objects.filter(number=transfer_number).first()):
        raise TransferNotFoundException()

    if transfer.type == TransferType.Withdraw:
        if transfer.to_bank_account and transfer.scheduled_at:
            if transfer.status == TransferStatus.Pending:
                data: Dict = {"transition": TransferTransitionTrigger.Cancel,
                              "transfer_number": transfer.number,
                              "schedule_id": str(transfer.schedule_id)}
                pub.send(f'transfer:{json.dumps(data)}'.encode('utf-8'))
