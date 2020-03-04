from django.urls import path

from frontend.views import (
    upload_page,
    metadata_list_page,
    get_metadata_list,
    metadata_detail,
    edit_metadata,
    delete_metadata,
    sign_in_page,
    logout)

urlpatterns = [
    path("", upload_page, name="upload-page"),
    path("login/", sign_in_page, name="login"),
    path("logout/", logout, name="logout"),
    path("metadata-list/", metadata_list_page, name="metadata-list-page"),
    path("get-metadata-list/", get_metadata_list, name="get-metadata-list"),
    path("metadata/<str:metadata_id>", metadata_detail, name="metadata-detail"),
    path("metadata/<str:metadata_id>/edit/", edit_metadata, name="edit-metadata"),
    path("metadata/<str:metadata_id>/delete/", delete_metadata, name="delete-metadata"),
]
