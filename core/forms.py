from __future__ import annotations
from django import forms
from .models import WorkEntry, MaterialEntry, Payment, Project, Asset




class ProjectPickerForm(forms.Form):
project = forms.ModelChoiceField(queryset=Project.objects.none(), label="Job")


def __init__(self, *args, **kwargs):
super().__init__(*args, **kwargs)
self.fields["project"].queryset = Project.objects.filter(is_active=True)




class WorkEntryForm(forms.ModelForm):
class Meta:
model = WorkEntry
fields = ["project", "asset", "date", "quantity", "notes"]
labels = {
"project": "Job",
"asset": "Resource",
"quantity": "Hours / Quantity",
}


def __init__(self, *args, **kwargs):
super().__init__(*args, **kwargs)
self.fields["asset"].queryset = Asset.objects.filter(is_active=True)
self.fields["project"].queryset = Project.objects.filter(is_active=True)




class MaterialEntryForm(forms.ModelForm):
class Meta:
model = MaterialEntry
fields = ["project", "date", "description", "cost", "markup_percent"]
labels = {"project": "Job", "markup_percent": "Markup % (override)"}




class PaymentForm(forms.ModelForm):
class Meta:
model = Payment
fields = ["project", "date", "amount", "reference"]
labels = {"project": "Job"}
