from __future__ import annotations

from django import forms

from .models import Asset, Client, MaterialEntry, Payment, Project, WorkEntry


DATE_FMT = "%m/%d/%Y"  # US format


class USDateInput(forms.DateInput):
    input_type = "text"

    def __init__(self, **kwargs):
        kwargs.setdefault("format", DATE_FMT)
        super().__init__(**kwargs)
        self.attrs.update({"placeholder": DATE_FMT, "autocomplete": "off"})


class ProjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: Project) -> str:
        return f"{obj.client.name} — {obj.name}"


class WorkEntryForm(forms.ModelForm):
    project = ProjectChoiceField(queryset=Project.objects.filter(active=True))

    class Meta:
        model = WorkEntry
        fields = ["project", "date", "hours", "asset", "notes"]
        widgets = {"date": USDateInput()}
        labels = {"asset": "Asset"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["asset"].queryset = Asset.objects.filter(active=True)
        # Filter assets by selected project's client
        proj = None
        if self.data.get("project"):
            try:
                proj = Project.objects.select_related("client").get(pk=self.data.get("project"))
            except Project.DoesNotExist:
                proj = None
        elif self.instance and self.instance.pk:
            proj = self.instance.project
        elif self.initial.get("project"):
            try:
                proj = Project.objects.select_related("client").get(pk=self.initial.get("project"))
            except Project.DoesNotExist:
                proj = None
        if proj:
            self.fields["asset"].queryset = Asset.objects.filter(client=proj.client, active=True)


class MaterialEntryForm(forms.ModelForm):
    project = ProjectChoiceField(queryset=Project.objects.filter(active=True))

    class Meta:
        model = MaterialEntry
        fields = ["project", "date", "description", "quantity", "unit_cost"]
        widgets = {"date": USDateInput()}


class PaymentForm(forms.ModelForm):
    project = ProjectChoiceField(queryset=Project.objects.filter(active=True))

    class Meta:
        model = Payment
        fields = ["project", "date", "amount", "notes"]
        widgets = {"date": USDateInput()}


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["client", "name", "active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(active=True)
