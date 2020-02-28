from django.urls import path

from service.views import UploadFileProcessingView

urlpatterns = [path("upload/", UploadFileProcessingView.as_view(), name="process-upload")]
