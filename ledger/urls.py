from django.urls import path

from .views import WalletLedgerEntryListView

app_name = 'ledger'

urlpatterns = [
    path("wallets/<int:wallet_id>/entries/", WalletLedgerEntryListView.as_view(), name="wallet_entries"),
]