from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Asset(models.Model):
    """Physical asset/equipment tracked by a client.

    NOTE: This model used to be referred to as "Resource" in UI copy. The
    canonical name is now Asset. Verbose names update the Admin language.
    """

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="assets", null=True, blank=True
    )  # why: allow null temporarily to avoid backfill breakage
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        unique_together = ("client", "name")
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        owner = self.client.name if self.client_id else "(no client)"
        return f"{self.name} — {owner}"


class Project(models.Model):  # UI name: Job
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Job"
        constraints = [
            models.UniqueConstraint(
                fields=["client", "name"], name="uniq_project_per_client"
            )
        ]
        ordering = ["client__name", "name"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} — {self.client.name}"


class RateOverride(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("project", "asset")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.project} / {self.asset}: {self.hourly_rate}"


class WorkEntry(models.Model):  # UI name: Labor & Equipment Log
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="work")
    date = models.DateField(default=timezone.now)
    hours = models.DecimalField(max_digits=7, decimal_places=2)
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date", "id"]


class MaterialEntry(models.Model):  # UI name: Material Log
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="materials")
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1"))
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["-date", "id"]

    @property
    def total(self) -> Decimal:
        return (self.quantity or Decimal("0")) * (self.unit_cost or Decimal("0"))


class Payment(models.Model):  # UI name: Payment Received
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date", "id"]


@dataclass
class ProjectTotals:
    labor: Decimal
    materials: Decimal
    payments: Decimal
    balance: Decimal

    @classmethod
    def for_project(cls, project: Project) -> "ProjectTotals":
        # Labor: hours * rate (override per-asset if exists)
        labor_total = Decimal("0.00")
        q = WorkEntry.objects.filter(project=project).select_related("asset")
        for w in q:
            rate = project.hourly_rate
            if w.asset_id:
                ro = RateOverride.objects.filter(project=project, asset=w.asset).first()
                if ro:
                    rate = ro.hourly_rate
            labor_total += (w.hours or Decimal("0")) * (rate or Decimal("0"))

        # Materials
        materials_total = Decimal("0.00")
        for m in MaterialEntry.objects.filter(project=project):
            materials_total += m.total

        # Payments
        payments_total = (
            Payment.objects.filter(project=project)
            .aggregate(s=models.Sum("amount"))
            .get("s")
            or Decimal("0.00")
        )

        balance = labor_total + materials_total - payments_total
        return cls(labor=labor_total, materials=materials_total, payments=payments_total, balance=balance)
