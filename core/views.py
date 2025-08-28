from __future__ import annotations
@login_required
def dashboard(request):
if request.method == "POST":
form = ProjectPickerForm(request.POST)
if form.is_valid():
project = form.cleaned_data["project"]
return redirect("core:report", project_id=project.id)
else:
form = ProjectPickerForm()
return render(request, "core/dashboard.html", {"form": form})




@login_required
def add_work_entry(request):
if request.method == "POST":
form = WorkEntryForm(request.POST)
if form.is_valid():
inst = form.save()
messages.success(request, f"Work entry saved: ${inst.line_total}")
return redirect(reverse("core:report", args=[inst.project_id]))
else:
form = WorkEntryForm()
return render(request, "core/work_entry_form.html", {"form": form})




@login_required
def add_material_entry(request):
if request.method == "POST":
form = MaterialEntryForm(request.POST)
if form.is_valid():
inst = form.save()
messages.success(request, f"Material entry saved: ${inst.sell_price}")
return redirect(reverse("core:report", args=[inst.project_id]))
else:
form = MaterialEntryForm()
return render(request, "core/material_entry_form.html", {"form": form})




@login_required
def add_payment(request):
if request.method == "POST":
form = PaymentForm(request.POST)
if form.is_valid():
inst = form.save()
messages.success(request, "Payment recorded")
return redirect(reverse("core:report", args=[inst.project_id]))
else:
form = PaymentForm()
return render(request, "core/payment_form.html", {"form": form})




@login_required
def report(request, project_id: int):
project = get_object_or_404(Project, pk=project_id)
totals = ProjectTotals(project)
ctx = {
"project": project,
"work_entries": project.work_entries.select_related("asset").order_by("date", "id"),
"material_entries": project.material_entries.order_by("date", "id"),
"payments": project.payments.order_by("date", "id"),
"totals": totals,
}
return render(request, "core/report.html", ctx)
