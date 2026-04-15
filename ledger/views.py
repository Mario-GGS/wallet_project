from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from wallets.models import Wallet
from .models import LedgerEntry
from .serializers import LedgerEntrySerializer

class WalletLedgerEntryListView(ListAPIView):
    serializer_class = LedgerEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        wallet_id = self.kwargs['wallet_id']

        wallet = get_object_or_404(
            Wallet,
            id=wallet_id,
            user=self.request.user,
        )

        return LedgerEntry.objects.filter(wallet=wallet).order_by('-created_at', "-id")