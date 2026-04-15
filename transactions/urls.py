from django.urls import path

from .views import DepositView, ReverseTransactionView, TransferView, WithdrawView

app_name = 'transactions'

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("transfer/", TransferView.as_view(), name="transfer"),
    path("reverse/", ReverseTransactionView.as_view(), name="reverse"),
]