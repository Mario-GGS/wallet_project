from rest_framework import serializers

from .models import LedgerEntry

class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = [
            "id",
            "wallet",
            "transaction",
            "direction",
            "amount",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "wallet",
            "transaction",
            "direction",
            "amount",
            "created_at",
        ]