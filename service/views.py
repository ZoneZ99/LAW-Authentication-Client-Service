import os

import requests
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()


class UploadFileProcessingView(APIView):
    def post(self, request, **params):
        file = request.data["uploaded_file"]
        COMPRESSION_SERVICE_URL = os.getenv("COMPRESSION_SERVICE_URL")
        response = requests.post(
            url=f"{COMPRESSION_SERVICE_URL}compress/",
            files={"file": open(file, "rb")}
        )
        return Response(data=response.json())
