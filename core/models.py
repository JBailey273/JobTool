from __future__ import annotations
from decimal import Decimal
from django.db import models
from django.utils import timezone


DECIMAL_OPTS = {"max_digits": 12, "decimal_places": 2}




class Customer(models.Model):
name = models.CharField(max_length=200, unique=True)
is_active = models.BooleanField(default=True)


class Meta:
verbose_name = "Contractor"
verbose_name_plural = "Contractors"


def __str__(self) -> str: # pragma: no cover
return self.name




class Client(models.Model):
customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="clients")
name = models.CharField(max_length=200)
is_active = models.BooleanField(default=True)


class Meta:
unique_together = ("customer", "name")
verbose_name = "Client"
verbose_name_plural = "Clients"


def __str__(self) -> str: # pragma: no cover
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
verbose_name = "Job"
verbose_name_plural = "Jobs"


def __str__(self) -> str: # pragma: no cover
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


class Meta:
verbose_name = "Resource"
verbose_name_plural = "Resources"


def __str__(self) -> str: # pragma: no cover
return self.name


return self.grand_total - self.payments_total
