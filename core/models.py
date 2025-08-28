from __future__ import annotations
from decimal import Decimal
from django.db import models
from django.utils import timezone

# Decimal field options reused across money/qty fields
DECIMAL_OPTS = {"max_digits": 12, "decimal_places": 2}


class Client(models.Model):
    """Your client. (Former Customer removed)"""

    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Project(models.Model):
    """A Job for a Client."""

    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, related_name="projects"
    )
    name = models.CharField(max_length=200)
    material_markup_percent = models.DecimalField(
        **DECIMAL_OPTS, default=Decimal("10.00")
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        unique_together = ("client", "name")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} — {self.client.name}"


class Asset(models.Model):
    """Equipment or Labor resource."""

    UNIT_HOUR = "hour"
    UNIT_DAY = "day"
    UNIT_EACH = "each"
    UNIT_CHOICES = [
        (UNIT_HOUR, "Hour"),
        (UNIT_DAY, "Day"),
        (UNIT_EACH, "Each"),
    ]

    name = models.CharField(max_length=200, unique=True)
    is_labor = models.BooleanField(default=False)
    unit = models.CharField(max_length=16, choices=UNIT_CHOICES, default=UNIT_HOUR)
    default_rate = models.DecimalField(**DECIMAL_OPTS, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class RateOverride(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="rate_overrides"
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="rate_overrides"
    )
    rate = models.DecimalField(**DECIMAL_OPTS)

    class Meta:
        unique_together = ("project", "asset")
        verbose_name = "Rate Override"
        verbose_name_plural = "Rate Overrides"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.project} / {self.asset}: {self.rate}"


class WorkEntry(models.Model):
    """Labor & Equipment log for a job."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="work_entries"
    )
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    quantity = models.DecimalField(**DECIMAL_OPTS, default=Decimal("0.00"))
    notes = models.TextField(blank=True)

    # Snapshotted pricing at save-time
    rate_used = models.DecimalField(
        **DECIMAL_OPTS, editable=False, default=Decimal("0.00")
    )
    line_total = models.DecimalField(
        **DECIMAL_OPTS, editable=False, default=Decimal("0.00")
    )

    class Meta:
        verbose_name = "Labor & Equipment Log"
        verbose_name_plural = "Labor & Equipment Logs"

    def _resolve_rate(self) -> Decimal:
        o = RateOverride.objects.filter(project=self.project, asset=self.asset).first()
        return o.rate if o else self.asset.default_rate

    def save(self, *args, **kwargs):  # compute snapshot values
        rate = self._resolve_rate()
        self.rate_used = rate
        qty = self.quantity or Decimal("0")
        self.line_total = (rate * qty).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.date} {self.asset} x {self.quantity} = {self.line_total}"


class MaterialEntry(models.Model):
    """Materials used on a job (with markup)."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="material_entries"
    )
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    cost = models.DecimalField(**DECIMAL_OPTS, default=Decimal("0.00"))
    markup_percent = models.DecimalField(
        **DECIMAL_OPTS, null=True, blank=True, help_text="Override job markup %"
    )

    # Snapshotted sell price at save-time
    sell_price = models.DecimalField(
        **DECIMAL_OPTS, editable=False, default=Decimal("0.00")
    )

    class Meta:
        verbose_name = "Material Log"
        verbose_name_plural = "Material Logs"

    def _effective_markup(self) -> Decimal:
        return (
            self.markup_percent
            if self.markup_percent is not None
            else self.project.material_markup_percent
        )

    def save(self, *args, **kwargs):
        m = self._effective_markup() or Decimal("0.00")
        self.sell_price = (
            self.cost * (Decimal("1.0") + (m / Decimal("100")))
        ).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.date} {self.description}: {self.sell_price}"


class Payment(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="payments"
    )
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(**DECIMAL_OPTS)
    reference = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Payment Received"
        verbose_name_plural = "Payments Received"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.date} ${self.amount} {self.reference}"


class ProjectTotals:
    """Convenience aggregator for reports."""

    def __init__(self, project: Project):
        self.project = project

    @property
    def work_total(self) -> Decimal:
        return sum(
            (w.line_total for w in self.project.work_entries.all()),
            Decimal("0.00"),
        )

    @property
    def materials_total(self) -> Decimal:
        return sum(
            (m.sell_price for m in self.project.material_entries.all()),
            Decimal("0.00"),
        )

    @property
    def payments_total(self) -> Decimal:
        return sum(
            (p.amount for p in self.project.payments.all()),
            Decimal("0.00"),
        )

    @property
    def grand_total(self) -> Decimal:
        return self.work_total + self.materials_total

    @property
    def balance_due(self) -> Decimal:
        return self.grand_total - self.payments_total
