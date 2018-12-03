from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("files/", views.files_index, name="files index"),
    path("files/<int:file_id>/", views.files_show, name="files-show"),
]
