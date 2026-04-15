from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from transactions.models import Transaction
from wallets.models import Wallet

class Hold(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RELEASED = "RELEASED", "Released"
        CAPTURED = "CAPTURED", "Captured"
        EXPIRED = "EXPIRED", "Expired"

    id = models.BigAutoField(primary_key=True)
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='holds',
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='holds',
    )
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'holds'
        constraints = [
            models.UniqueConstraint(
                fields=["transaction"],
                name="uq_hold_transaction",
            )
        ]
        indexes = [
            models.Index(fields=["wallet", "status"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.wallet_id} - {self.transaction_id} - {self.status} - {self.amount}"