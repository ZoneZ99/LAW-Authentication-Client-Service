import os

import requests
from django.http import JsonResponse, HttpResponseNotAllowed, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework import status

from frontend.forms import UploadFileForm

load_dotenv()

COMPRESSION_SERVICE_URL = os.getenv("COMPRESSION_SERVICE_URL")
METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")


def process_uploaded_file(file):
    requests.post(
        url=f"{COMPRESSION_SERVICE_URL}compress/",
        files={"file": file.file},
        data={"filename": file.name},
    )
    return redirect(reverse("metadata-list-page"))


def upload_page(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return process_uploaded_file(request.FILES["file"])
        else:
            form = UploadFileForm(request.POST, request.FILES)
    else:
        form = UploadFileForm()
    return render(request, template_name="upload-page.html", context={"form": form})


def metadata_list_page(request):
    return render(request, "metadata-list.html")


def get_metadata_list(request):
    if request.method == "GET":
        response = requests.get(url=f"{METADATA_SERVICE_URL}metadata/")
        return JsonResponse(data={"metadata": response.json()})
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


def metadata_detail(request, metadata_id):
    if request.method == "GET":
        detail = requests.get(
            url=f"{METADATA_SERVICE_URL}metadata/{metadata_id}/"
        ).json()
        return render(request, "metadata-detail.html", {"metadata": detail})
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


def edit_metadata(request, metadata_id):
    if request.method == "PATCH":
        data = QueryDict(request.body)
        response = requests.patch(
            url=f"{METADATA_SERVICE_URL}metadata/{metadata_id}/",
            data={"name": data["name"], "description": data["description"],},
        )
        return JsonResponse(data=response.json(), status=status.HTTP_200_OK)
    else:
        return HttpResponseNotAllowed(permitted_methods=["PATCH"])


def delete_metadata(request, metadata_id):
    if request.method == "DELETE":
        requests.delete(url=f"{METADATA_SERVICE_URL}metadata/{metadata_id}/")
        return JsonResponse(data={}, status=status.HTTP_200_OK)
    else:
        return HttpResponseNotAllowed(permitted_methods=["DELETE"])
