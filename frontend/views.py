import os

import requests
from django.http import JsonResponse
from django.shortcuts import render

from frontend.forms import UploadFileForm


def process_uploaded_file(file):
    # file = open(file, "rb")
    COMPRESSION_SERVICE_URL = os.getenv("COMPRESSION_SERVICE_URL")
    print(file.name)
    response = requests.post(
        url=f"{COMPRESSION_SERVICE_URL}compress/",
        files={"file": file.file},
        data={"filename": file.name}
    )
    return JsonResponse(data=response.json())


def upload_page(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return process_uploaded_file(request.FILES["file"])
    else:
        form = UploadFileForm()
    return render(
        request,
        template_name="upload-page.html",
        context={"form": form}
    )
