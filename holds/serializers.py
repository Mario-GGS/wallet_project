from rest_framework import serializers
from .models import Hold

class HoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hold
        fields = [
            "id",
            "wallet",
            "transaction",
            "amount",
            "status",
            "expires_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "wallet",
            "transaction",
            "amount",
            "status",
            "expires_at",
            "created_at",
        ]

class AmountValidationMixin:
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

class CreateHoldSerializer(AmountValidationMixin, serializers.Serializer):
    wallet_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    idempotency_key = serializers.CharField(max_length=128)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    metadata = serializers.JSONField(required=False, default=dict)

class ReleaseHoldSerializer(serializers.Serializer):
    idempotency_key = serializers.CharField(max_length=128)
    metadata = serializers.JSONField(required=False, default=dict)

class CaptureHoldSerializer(serializers.Serializer):
    idempotency_key = serializers.CharField(max_length=128)
    metadata = serializers.JSONField(required=False, default=dict)