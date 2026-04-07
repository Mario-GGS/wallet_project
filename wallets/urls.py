from django.urls import path
from .views import WalletDetailView, WalletBalanceView

app_name = "wallets"

urlpatterns = [
    path("<int:wallet_id>/", WalletDetailView.as_view(), name="wallet_detail"),
    path("<int:wallet_id>/balance/", WalletBalanceView.as_view(), name="wallet_balance"),
]