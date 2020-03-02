from django.urls import path

from frontend.views import upload_page, metadata_list_page, get_metadata_list, metadata_detail

urlpatterns = [
    path("", upload_page, name="upload-page"),
    path("metadata-list/", metadata_list_page, name="metadata-list-page"),
    path("get-metadata-list/", get_metadata_list, name="get-metadata-list"),
    path("metadata/<str:metadata_id>", metadata_detail, name="metadata-detail"),
]
