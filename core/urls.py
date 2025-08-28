from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView

def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path(
        "login/",
        LoginView.as_view(
            template_name="account/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
