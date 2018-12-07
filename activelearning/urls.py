"""activelearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from ensemble.urls import urlpatterns as ensemble_urls

# Custom admin site title/header
admin.site.site_title = "Active Learning"
admin.site.site_header = "Active Learning Management"

urlpatterns = (
    [path("", include("ensemble.urls"))]
    + [path("ensemble/", include("ensemble.urls")), path("admin/", admin.site.urls)]
    + ensemble_urls
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
