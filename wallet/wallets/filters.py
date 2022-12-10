from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request
from rest_framework.views import View


class WalletFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View):
        return queryset.filter(client_id=view.kwargs.get("client_id"))


class TransferFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view: View):
        print(view.kwargs.get("client_id"))
        return queryset.filter(client_id=view.kwargs.get("client_id"))
