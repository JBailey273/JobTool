from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect

def root(request):
    return HttpResponseRedirect("/login/") if not request.user.is_authenticated else HttpResponseRedirect("/admin/")

urlpatterns = [
    path("", root, name="root"),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
