from rest_framework import serializers
from .models import Transaction, TransactionWalletLink

class TransactionWalletLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionWalletLink
        fields = ["id", "wallet", "role", "created_at"]
        read_only_fields = ["id", "wallet", "role", "created_at"]

class TransactionSerializer(serializers.ModelSerializer):
    wallet_links = TransactionWalletLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "actor_user",
            "type",
            "status",
            "reversal_of",
            "idempotency_key",
            "metadata",
            "created_at",
            "wallet_links",
        ]
        read_only_fields = [
            "id",
            "actor_user",
            "type",
            "status",
            "reversal_of",
            "created_at",
            "wallet_links",
        ]

class ValidateAmountMixin:
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

class DepositSerializer(ValidateAmountMixin, serializers.Serializer):
    wallet_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    idempotency_key = serializers.CharField(max_length=128)
    metadata = serializers.JSONField(required=False, default=dict)


class WithdrawSerializer(ValidateAmountMixin, serializers.Serializer):
    wallet_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    idempotency_key = serializers.CharField(max_length=128)
    metadata = serializers.JSONField(required=False, default=dict)


class TransferSerializer(ValidateAmountMixin, serializers.Serializer):
    from_wallet_id = serializers.IntegerField(min_value=1)
    to_wallet_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    idempotency_key = serializers.CharField(max_length=128)
    metadata = serializers.JSONField(required=False, default=dict)

    def validate(self, attrs):
        if attrs["from_wallet_id"] == attrs["to_wallet_id"]:
            raise serializers.ValidationError(
                "Source wallet and destination wallet must be different"
            )
        return attrs

class ReverseTransactionSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()
    idempotency_key = serializers.CharField(max_length=128)
    metadata = serializers.JSONField(required=False, default=dict)