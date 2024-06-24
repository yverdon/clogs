"""
URL configuration for clogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django_oapif.urls import oapif_router

from clogs.core import views as core_views
from clogs.themes.api import api

urlpatterns = [
    path("", core_views.home, name="home"),
    path("clone-geoportal", core_views.clone_geoportal, name="clone_geoportal"),
    path("admin/", admin.site.urls, {"extra_context": {"DEBUG": settings.DEBUG}}),
    path("oapif/", include(oapif_router.urls)),
    path("users/", include("allauth.urls")),
    path(
        "api/",
        api.urls,
    ),
]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
