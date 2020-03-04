import os
from datetime import datetime, timedelta

import requests
from django.http import JsonResponse, HttpResponseNotAllowed, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework import status

from frontend.decorators import LAW_login_required
from frontend.forms import UploadFileForm, LAWAuthenticationForm

load_dotenv()

COMPRESSION_SERVICE_URL = os.getenv("COMPRESSION_SERVICE_URL")
METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")


def sign_in_page(request):
    if request.method == "GET":
        form = LAWAuthenticationForm()
        return render(request, "sign-in.html", {"form": form})
    elif request.method == "POST":
        form = LAWAuthenticationForm(request.POST)
        if form.is_valid():
            oauth_response = requests.post(
                url="http://oauth.infralabs.cs.ui.ac.id/oauth/token",
                data={
                    "username": form.cleaned_data["username"],
                    "password": form.cleaned_data["password"],
                    "client_id": form.cleaned_data["client_id"],
                    "client_secret": form.cleaned_data["client_secret"],
                    "grant_type": "password",
                },
            )
            if oauth_response.status_code == status.HTTP_400_BAD_REQUEST:
                form = LAWAuthenticationForm(request.POST)
                return render(request, "sign-in.html", {"form": form})
            elif oauth_response.status_code == status.HTTP_200_OK:
                oauth_response = oauth_response.json()
                request.session["access_token"] = oauth_response["access_token"]
                request.session["expires_in"] = (
                    datetime.now() + timedelta(seconds=oauth_response["expires_in"])
                ).strftime("%m/%d/%y %H:%M:%S")
                request.session["user_id"] = form.cleaned_data["username"]
                return redirect(reverse("metadata-list-page"))
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET", "POST"])


def process_uploaded_file(file):
    requests.post(
        url=f"{COMPRESSION_SERVICE_URL}compress/",
        files={"file": file.file},
        data={"filename": file.name},
    )
    return redirect(reverse("metadata-list-page"))


@LAW_login_required
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


@LAW_login_required
def metadata_list_page(request):
    return render(request, "metadata-list.html")


@LAW_login_required
def get_metadata_list(request):
    if request.method == "GET":
        response = requests.get(url=f"{METADATA_SERVICE_URL}metadata/")
        return JsonResponse(data={"metadata": response.json()})
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@LAW_login_required
def metadata_detail(request, metadata_id):
    if request.method == "GET":
        detail = requests.get(
            url=f"{METADATA_SERVICE_URL}metadata/{metadata_id}/"
        ).json()
        return render(request, "metadata-detail.html", {"metadata": detail})
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@LAW_login_required
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


@LAW_login_required
def delete_metadata(request, metadata_id):
    if request.method == "DELETE":
        requests.delete(url=f"{METADATA_SERVICE_URL}metadata/{metadata_id}/")
        return JsonResponse(data={}, status=status.HTTP_200_OK)
    else:
        return HttpResponseNotAllowed(permitted_methods=["DELETE"])
