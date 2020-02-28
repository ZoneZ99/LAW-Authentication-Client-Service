from django.urls import path

from frontend.views import upload_page

urlpatterns = [path("", upload_page, name="upload-page")]
