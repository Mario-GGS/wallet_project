from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, DecimalField, Value
from django.db.models.functions import Coalesce
# Coalesce if value return None equals to 0

from .models import Wallet
from ledger.models import LedgerEntry
from holds.models import Hold

def get_wallet_handler(*, wallet_id, user):
    return get_object_or_404(
        Wallet,
        id=wallet_id,
        user=user,
    )

def get_total_balance_handler(*, wallet):
    totals = LedgerEntry.objects.filter(wallet=wallet).aggregate(
        credits=Coalesce(
            Sum("amount", filter=Q(direction="CREDIT")),
            Value(0),
            output_field=DecimalField(max_digits=18, decimal_places=2),
        ),
        debits=Coalesce(
            Sum("amount", filter=Q(direction="DEBIT")),
            Value(0),
            output_field=DecimalField(max_digits=18, decimal_places=2),
        ),
    )
    return totals["credits"] - totals["debits"]

def get_held_balance_handler(*, wallet):
    held_balance = Hold.objects.filter(
        wallet=wallet,
        status="ACTIVE",
    ).aggregate(
        total=Coalesce(
            Sum("amount"),
            Value(0),
            output_field=DecimalField(max_digits=18, decimal_places=2),
        )
    )["total"]

    return held_balance

def get_available_balance_handler(*, wallet):
    total_balance = get_total_balance_handler(wallet=wallet)
    held_balance = get_held_balance_handler(wallet=wallet)
    return total_balance - held_balance

def get_wallet_balance_summary_handler(*, wallet):
    total_balance = get_total_balance_handler(wallet=wallet)
    held_balance = get_held_balance_handler(wallet=wallet)
    available_balance = total_balance - held_balance

    return {
        "wallet_id": wallet.id,
        "currency": wallet.currency,
        "total_balance": total_balance,
        "held_balance": held_balance,
        "available_balance": available_balance,
    }
