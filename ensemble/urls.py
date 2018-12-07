from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.files_index, name="index"),
    path("files/", views.files_index, name="files index"),
    path("files/<int:file_id>/", views.files_show, name="files-show"),
    path("files/<int:file_id>/compare", views.files_compare, name="files-compare"),
]
