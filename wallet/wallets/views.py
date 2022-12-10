from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView

from wallets.filters import WalletFilterBackend, TransferFilterBackend
from wallets.models import Wallet, Transfer
from wallets.serializers import WalletSerializer, CreateTransferSerializer, UpdateTransferSerializer


class CreateWalletView(CreateAPIView):
    serializer_class = WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    filter_backends = (WalletFilterBackend,)
    lookup_field = "uuid"
    lookup_url_kwarg = "wallet_id"


class CreateTransferView(CreateAPIView):
    serializer_class = CreateTransferSerializer


class RetrieveUpdateTransferView(RetrieveUpdateAPIView):
    serializer_class = UpdateTransferSerializer
    queryset = Transfer.objects.all()
    filter_backends = (TransferFilterBackend,)
    lookup_field = "number"
