from django.urls import path

from wallets.views import CreateWalletView, RetrieveWalletView, CreateTransferView, RetrieveUpdateTransferView

urlpatterns = [
    path("clients/<slug:client_id>/wallets", CreateWalletView.as_view()),
    path("clients/<slug:client_id>/wallets/<slug:wallet_id>/", RetrieveWalletView.as_view()),
    path("clients/<slug:client_id>/wallets/<slug:wallet_id>/transfers", CreateTransferView.as_view()),
    path("clients/<slug:client_id>/wallets/<slug:wallet_id>/transfers/<slug:number>", RetrieveUpdateTransferView.as_view()),
]
