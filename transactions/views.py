from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import handlers
from .serializers import (
    DepositSerializer,
    ReverseTransactionSerializer,
    TransactionSerializer,
    TransferSerializer,
    WithdrawSerializer
)

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = handlers.deposit_handler(
            actor_user=request.user,
            **serializer.validated_data
        )

        response_serializer = TransactionSerializer(transaction)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = handlers.withdraw_handler(
            actor_user=request.user,
            **serializer.validated_data
        )
        response_serializer = TransactionSerializer(transaction)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = handlers.transfer_handler(
            actor_user=request.user,
            **serializer.validated_data
        )
        response_serializer = TransactionSerializer(transaction)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class ReverseTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReverseTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = handlers.reverse_transaction_handler(
            actor_user=request.user,
            **serializer.validated_data
        )
        response_serializer = TransactionSerializer(transaction)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

