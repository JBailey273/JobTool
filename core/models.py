from __future__ import annotations
m = self._effective_markup() or Decimal("0.00")
self.sell_price = (self.cost * (Decimal("1.0") + (m / Decimal("100")))).quantize(Decimal("0.01"))
super().save(*args, **kwargs)


def __str__(self) -> str: # pragma: no cover
return f"{self.date} {self.description}: {self.sell_price}"


class Payment(models.Model):
project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="payments")
date = models.DateField(default=timezone.now)
amount = models.DecimalField(**DECIMAL_OPTS)
reference = models.CharField(max_length=200, blank=True)


class Meta:
verbose_name = "Payment Received"
verbose_name_plural = "Payments Received"


def __str__(self) -> str: # pragma: no cover
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
