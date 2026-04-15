import uuid
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from wallets.models import Wallet

class Transaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAW = "WITHDRAW", "Withdraw"
        TRANSFER = "TRANSFER", "Transfer"
        HOLD = "HOLD", "Hold"
        RELEASE = "RELEASE", "Release"
        CAPTURE = "CAPTURE", "Capture"
        REVERSAL = "REVERSAL", "Reversal"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        POSTED = "POSTED", "Posted"
        REVERSED = "REVERSED", "Reversed"
        FAILED = "FAILED", "Failed"


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    type = models.CharField(
        max_length=30,
        choices=Type,
    )
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.POSTED
    )
    reversal_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reversals",
    )
    idempotency_key = models.CharField(max_length=128)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "transactions"
        constraints = [
            models.UniqueConstraint(
                fields=["actor_user", "type", "idempotency_key"],
                name="uq_tx_actor_type_idemkey",
            )
        ]
        indexes = [
            models.Index(fields=["actor_user"]),
            models.Index(fields=["type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["reversal_of"]),
        ]

    def __str__(self):
        return f"{self.id} - {self.type} - {self.status}"

class TransactionWalletLink(models.Model):
    class Role(models.TextChoices):
        SOURCE = "SOURCE", "Source"
        DESTINATION = "DESTINATION", "Destination"
        AFFECTED = "AFFECTED", "Affected"

    id = models.BigAutoField(primary_key=True)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="wallet_links",
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transaction_links",
    )
    role = models.CharField(
        max_length=20,
        choices=Role,
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "transaction_wallet_links"
        constraints = [
            models.UniqueConstraint(
                fields=["transaction", "wallet"],
                name="uq_tx_wallet_unique",
            )
        ]
        indexes = [
            models.Index(fields=["transaction"]),
            models.Index(fields=["wallet"]),
            models.Index(fields=["transaction","role"]),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.wallet_id} - {self.role}"