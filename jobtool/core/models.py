from __future__ import annotations
from decimal import Decimal
from django.db import models
from django.utils import timezone

DECIMAL_OPTS = {"max_digits": 12, "decimal_places": 2}

class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name

class Client(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("customer", "name")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.customer.name})"

class Project(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="projects")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="projects")
    name = models.CharField(max_length=200)
    material_markup_percent = models.DecimalField(**DECIMAL_OPTS, default=Decimal("10.00"))
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("customer", "client", "name")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} — {self.client.name} / {self.customer.name}"

class Asset(models.Model):
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

    def __str__(self) -> str:  # pragma: no cover
        return self.name

class RateOverride(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rate_overrides")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="rate_overrides")
    rate = models.DecimalField(**DECIMAL_OPTS)

    class Meta:
        unique_together = ("project", "asset")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.project} / {self.asset}: {self.rate}"

class WorkEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="work_entries")
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    quantity = models.DecimalField(**DECIMAL_OPTS, default=Decimal("0.00"))
    notes = models.TextField(blank=True)

    rate_used = models.DecimalField(**DECIMAL_OPTS, editable=False, default=Decimal("0.00"))
    line_total = models.DecimalField(**DECIMAL_OPTS, editable=False, default=Decimal("0.00"))

    def _resolve_rate(self) -> Decimal:
        o = RateOverride.objects.filter(project=self.project, asset=self.asset).first()
        return o.rate if o else self.asset.default_rate

    def save(self, *args, **kwargs):  # computes snapshot values
        rate = self._resolve_rate()
        self.rate_used = rate
        self.line_total = (rate * (self.quantity or Decimal("0"))).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.date} {self.asset} x {self.quantity} = {self.line_total}"

class MaterialEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="material_entries")
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    cost = models.DecimalField(**DECIMAL_OPTS, default=Decimal("0.00"))
    markup_percent = models.DecimalField(**DECIMAL_OPTS, null=True, blank=True, help_text="Override project markup %")

    sell_price = models.DecimalField(**DECIMAL_OPTS, editable=False, default=Decimal("0.00"))

    def _effective_markup(self) -> Decimal:
        return (self.markup_percent if self.markup_percent is not None else self.project.material_markup_percent)

    def save(self, *args, **kwargs):
        m = self._effective_markup() or Decimal("0.00")
        self.sell_price = (self.cost * (Decimal("1.0") + (m / Decimal("100")))).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.date} {self.description}: {self.sell_price}"

class Payment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(**DECIMAL_OPTS)
    reference = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.date} ${self.amount} {self.reference}"

# Aggregation helpers for reporting
class ProjectTotals:
    def __init__(self, project: Project):
        self.project = project

    @property
    def work_total(self) -> Decimal:
        return sum((w.line_total for w in self.project.work_entries.all()), Decimal("0.00"))

    @property
    def materials_total(self) -> Decimal:
        return sum((m.sell_price for m in self.project.material_entries.all()), Decimal("0.00"))

    @property
    def payments_total(self) -> Decimal:
        return sum((p.amount for p in self.project.payments.all()), Decimal("0.00"))

    @property
    def grand_total(self) -> Decimal:
        return self.work_total + self.materials_total

    @property
    def balance_due(self) -> Decimal:
        return self.grand_total - self.payments_total
