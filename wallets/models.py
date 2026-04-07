from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

class Wallet(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_FROZEN = "FROZEN"
    STATUS_CLOSED = "CLOSED"

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_FROZEN, "Frozen"),
        (STATUS_CLOSED, "Closed"),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="wallets",
    )
    currency = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "wallets"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "currency"],
                name="uq_wallet_user_currency",
            )
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["currency"]),
            models.Index(fields=["status"])
        ]

    def __str__(self):
        return f"{self.user.email} - {self.currency} ({self.status})"