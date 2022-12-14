from __future__ import annotations

from datetime import datetime
from typing import Dict, Any

from banks.models import Client
from dto_pack import TransferType, TransferTransitionTrigger
from rest_framework import serializers
from wallets.exceptions import ClientNotFoundException, WalletConflictException
from wallets.models import Wallet, Transfer, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("uuid", "client", "balance")
        read_only_fields = ("uuid", "client", "balance")

    def create(self, validated_data: Dict[str, Any]):
        client_id: str = self.context["view"].kwargs["client_id"]

        if not (client := Client.objects.filter(uuid=client_id).first()):
            raise ClientNotFoundException()
        if Wallet.objects.filter(client=client).first():
            raise WalletConflictException()

        validated_data["client"] = client

        return super().create(validated_data)


class CreateTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = ("number", "status", "type", "amount", "transaction", "from_bank_account", "to_bank_account", "created_at", "schedule_id", "scheduled_at", "finished_at", "canceled_at")
        read_only_fields = ("number", "status", "transaction", "schedule_id", "created_at", "finished_at", "canceled_at")

    def create(self, validated_data: Dict[str, Any]):
        client_id: str = self.context["view"].kwargs["client_id"]

        if not (client := Client.objects.filter(uuid=client_id).first()):
            raise ClientNotFoundException()

        if validated_data.get("type") == TransferType.Deposit and validated_data.get("scheduled_at"):
            validated_data.pop("scheduled_at")

        validated_data["client"] = client
        validated_data["finished_at"] = datetime.now()

        instance: Transfer = super().create(validated_data)

        return instance.change_transfer_state(TransferTransitionTrigger.Submit)


class UpdateTransferSerializer(serializers.ModelSerializer):
    transition = serializers.CharField(max_length=10, write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = Transfer
        fields = ("number", "status", "type", "amount", "transaction", "from_bank_account", "to_bank_account", "created_at", "schedule_id","scheduled_at", "finished_at", "canceled_at", "transition")
        read_only_fields = ("number", "status", "type", "amount", "transaction", "from_bank_account", "to_bank_account", "created_at", "schedule_id", "scheduled_at", "finished_at", "canceled_at")

    def update(self, transfer: Transfer, validated_data: Dict[str, Any]):
        return transfer.change_transfer_state(validated_data.pop("transition"))
