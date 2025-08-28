from __future__ import annotations
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import ProjectPickerForm, WorkEntryForm, MaterialEntryForm, PaymentForm
from .models import Project, ProjectTotals




def healthz(_request):
return HttpResponse("ok", content_type="text/plain")




def root(request):
# Simple, explicit redirect to avoid any middleware surprises
if request.user.is_authenticated:
return redirect("core:dashboard")
return redirect("core:login")




class BrandedLoginView(LoginView):
template_name = "account/login.html"
redirect_authenticated_user = True


def form_valid(self, form):
# Remember me keeps session for 30 days; else browser session only.
remember = self.request.POST.get("remember")
if remember:
self.request.session.set_expiry(60 * 60 * 24 * 30)
else:
self.request.session.set_expiry(0)
return super().form_valid(form)




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
return render(request, "core/report.html", ctx)
