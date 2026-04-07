from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import WalletSerializer, WalletBalanceSerializer
from .handler import (
    get_wallet_handler,
    get_wallet_balance_summary_handler
)

class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, wallet_id):
        wallet = get_wallet_handler(
            wallet_id=wallet_id,
            user=request.user,
        )
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, wallet_id):
        wallet = get_wallet_handler(
            wallet_id=wallet_id,
            user=request.user,
        )
        balance_data = get_wallet_balance_summary_handler(wallet=wallet)
        serializer = WalletBalanceSerializer(balance_data)
        return Response(serializer.data)
