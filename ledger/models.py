from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal

from transactions.models import Transaction
from wallets.models import Wallet

class LedgerEntry(models.Model):
    class Direction(models.TextChoices):
        CREDIT = "CREDIT", "Credit"
        DEBIT = "DEBIT", "Debit"

    id = models.BigAutoField(primary_key=True)
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="ledger_entries",
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="ledger_entries",
    )
    direction = models.CharField(
        max_length=10,
        choices=Direction.choices,
    )
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "ledger_entries"
        indexes = [
            models.Index(fields=["wallet", "created_at"]),
            models.Index(fields=["transaction"]),
            models.Index(fields=["wallet", "transaction"]),
            models.Index(fields=["direction"]),
        ]

    def __str__(self):
        return f"{self.wallet_id} - {self.transaction_id} - {self.direction} - {self.amount}"
