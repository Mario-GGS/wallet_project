from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    """
    Lectura: Muestra los datos de un wallet
    """
    class Meta:
        model = Wallet
        fields = ["id", "user", "currency", "status", "created_at"]
        read_only_fields = ["id", "created_at"]

class WalletBalanceSerializer(serializers.Serializer):
    wallet_id = serializers.IntegerField(read_only=True)
    currency = serializers.CharField(read_only=True)
    total_balance = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )
    held_balance = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )
    available_balance = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )